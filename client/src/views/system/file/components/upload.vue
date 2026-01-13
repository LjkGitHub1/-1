<script lang="ts" setup>
import { onMounted, ref } from "vue";
import type {
  UploadFile,
  UploadProgressEvent,
  UploadRawFile,
  UploadRequestOptions
} from "element-plus";
import { systemUploadFileApi } from "@/api/system/file";
import { searchUserApi } from "@/api/system/search";
import { message } from "@/utils/message";
import { useI18n } from "vue-i18n";
import { UploadFilled } from "@element-plus/icons-vue";
import { FieldValues, PlusColumn } from "plus-pro-components";
import { formatBytes, throttle } from "@pureadmin/utils";
import { hasAuth } from "@/router/utils";

interface AddOrEditFormProps {
  formInline?: FieldValues;
  formProps?: object;
  columns?: PlusColumn[];
  tableRef?: any;
}

const props = withDefaults(defineProps<AddOrEditFormProps>(), {
  formInline: () => ({}),
  formProps: () => ({}),
  columns: () => [],
  tableRef: undefined
});

defineOptions({ name: "UploadFile" });

const { t } = useI18n();
const fileList = ref<UploadFile[]>([]);
const uploadConfig = ref({ file_upload_size: 1048576 });
const selectedUserId = ref<number | null>(null);
const fileDescription = ref<string>("");
const userOptions = ref<
  Array<{
    pk: number;
    username: string;
    nickname: string;
    medical_record_no?: string;
  }>
>([]);
const userLoading = ref(false);
const uploading = ref(false);
const uploadRef = ref();

onMounted(() => {
  if (hasAuth("config:SystemUploadFile")) {
    systemUploadFileApi.config().then(res => {
      if (res.code === 1000) {
        uploadConfig.value = res.data;
      }
    });
  }
  // 加载用户列表（只获取普通用户，排除超级管理员）
  loadUsers();
});

const loadUsers = async () => {
  userLoading.value = true;
  try {
    const res = await searchUserApi.list({ is_active: true, page_size: 1000 });
    if (res.code === 1000 && res.data?.results) {
      // 过滤掉超级管理员，只显示普通用户
      userOptions.value = res.data.results.filter(
        (user: any) => !user.is_superuser
      );
    }
  } catch (error) {
    console.error("加载用户列表失败:", error);
  } finally {
    userLoading.value = false;
  }
};

const uploadRequest = (option: UploadRequestOptions) => {
  const data = new FormData();
  data.append("file", option.file);
  if (selectedUserId.value) {
    data.append("user_id", selectedUserId.value.toString());
  }
  if (fileDescription.value) {
    data.append("description", fileDescription.value);
  }
  return systemUploadFileApi.upload(data, {
    onUploadProgress: (event: any) => {
      const progressEvt = event as UploadProgressEvent;
      progressEvt.percent =
        event.total > 0 ? (event.loaded / event.total) * 100 : 0;
      option.onProgress(progressEvt);
    }
  });
};

const refreshData = throttle(props.tableRef?.handleGetData, 2000);

const beforeUpload = (rawFile: UploadRawFile) => {
  if (rawFile.size > uploadConfig.value.file_upload_size) {
    message(
      `${rawFile.name} ${t("systemUploadFile.uploadTip")} ${formatBytes(uploadConfig.value.file_upload_size)}!`,
      { type: "warning" }
    );
    return false;
  }
  return true;
};

// 手动上传所有文件
const handleUpload = async () => {
  // 验证必填项
  if (!selectedUserId.value) {
    message(t("systemUploadFile.selectUserRequired"), { type: "warning" });
    return;
  }

  if (fileList.value.length === 0) {
    message(t("systemUploadFile.selectFileRequired"), { type: "warning" });
    return;
  }

  // 验证文件大小
  const invalidFiles = fileList.value.filter(file => {
    const rawFile = file.raw as UploadRawFile;
    return rawFile && rawFile.size > uploadConfig.value.file_upload_size;
  });

  if (invalidFiles.length > 0) {
    message(
      t("systemUploadFile.uploadTip") +
        " " +
        formatBytes(uploadConfig.value.file_upload_size) +
        "!",
      { type: "warning" }
    );
    return;
  }

  uploading.value = true;
  let successCount = 0;
  let failCount = 0;

  try {
    // 逐个上传文件
    for (const file of fileList.value) {
      if (file.status === "success") continue; // 跳过已上传的文件

      const rawFile = file.raw as UploadRawFile;
      if (!rawFile) continue;

      try {
        const data = new FormData();
        data.append("file", rawFile);
        data.append("user_id", selectedUserId.value!.toString());
        if (fileDescription.value) {
          data.append("description", fileDescription.value);
        }

        const response = await systemUploadFileApi.upload(data);

        if (response.code === 1000) {
          file.status = "success";
          successCount++;
        } else {
          file.status = "fail";
          failCount++;
          message(`${file.name} ${t("results.failed")}：${response.detail}`, {
            type: "error"
          });
        }
      } catch (error: any) {
        file.status = "fail";
        failCount++;
        message(
          `${file.name} ${t("results.failed")}：${error.message || error}`,
          {
            type: "error"
          }
        );
      }
    }

    // 显示上传结果
    if (successCount > 0) {
      message(
        t("systemUploadFile.uploadSuccess").replace(
          "{count}",
          successCount.toString()
        ),
        { type: "success" }
      );
      refreshData();
      // 清空表单
      fileList.value = [];
      selectedUserId.value = null;
      fileDescription.value = "";
    }
  } finally {
    uploading.value = false;
  }
};
</script>

<template>
  <el-scrollbar max-height="600px">
    <div class="p-4">
      <el-form
        :model="{ user: selectedUserId, description: fileDescription }"
        label-width="100px"
      >
        <el-form-item :label="t('systemUploadFile.selectUser')">
          <el-select
            v-model="selectedUserId"
            :placeholder="t('systemUploadFile.selectUserPlaceholder')"
            filterable
            clearable
            :loading="userLoading"
            style="width: 100%"
          >
            <el-option
              v-for="user in userOptions"
              :key="user.pk"
              :label="`${user.nickname || user.username}${user.medical_record_no ? ` (${user.medical_record_no})` : ''}`"
              :value="user.pk"
            >
              <span>{{ user.nickname || user.username }}</span>
              <span
                v-if="user.medical_record_no"
                style=" margin-left: 8px; font-size: 12px;color: #8492a6"
              >
                ({{ user.medical_record_no }})
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item :label="t('systemUploadFile.fileDescription')">
          <el-input
            v-model="fileDescription"
            type="textarea"
            :rows="3"
            :placeholder="t('systemUploadFile.fileDescriptionPlaceholder')"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <el-upload
        ref="uploadRef"
        v-model:file-list="fileList"
        :before-upload="beforeUpload"
        :auto-upload="false"
        class="mt-4"
        drag
        multiple
      >
        <el-icon class="el-icon--upload">
          <UploadFilled />
        </el-icon>
        <div class="el-upload__text">
          {{ t("systemUploadFile.dropFile") }}
          <em>{{ t("systemUploadFile.clickUpload") }}</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            {{ t("systemUploadFile.uploadTip") }}
            {{ formatBytes(uploadConfig.file_upload_size) }}
          </div>
        </template>
      </el-upload>
      <div class="mt-4 text-right">
        <el-button
          @click="
            fileList = [];
            selectedUserId = null;
            fileDescription = '';
          "
        >
          {{ t("labels.reset") }}
        </el-button>
        <el-button
          type="primary"
          :loading="uploading"
          :disabled="fileList.length === 0 || !selectedUserId"
          @click="handleUpload"
        >
          {{ t("labels.confirm") }}
        </el-button>
      </div>
    </div>
  </el-scrollbar>
</template>
