<template>
  <div v-loading="loading" class="art-therapy-workflow-container">
    <div class="page-header mb-4">
      <div class="header-content">
        <h2 class="page-title">艺术治疗全流程辅助系统</h2>
        <div class="header-actions">
          <el-button
            type="primary"
            :disabled="uploadedFiles.length === 0"
            @click="handleRunWorkflow"
          >
            <template #icon
              ><el-icon><Play /></el-icon
            ></template>
            执行工作流
          </el-button>
          <el-button :disabled="uploadedFiles.length === 0" @click="clearFiles">
            <template #icon
              ><el-icon><Refresh /></el-icon
            ></template>
            清空图片
          </el-button>
        </div>
      </div>
    </div>

    <div class="workflow-content">
      <!-- 圖片上傳區域 -->
      <el-card class="upload-card mb-6" shadow="never">
        <template #header>
          <span>图片上传</span>
        </template>

        <el-upload
          v-model:file-list="fileList"
          :http-request="handleUploadRequest"
          :on-remove="handleRemove"
          :before-upload="beforeUpload"
          list-type="picture-card"
          :limit="10"
          accept="image/*"
          multiple
        >
          <el-icon><Plus /></el-icon>
        </el-upload>

        <div v-if="uploadedFiles.length === 0" class="upload-tip">
          <el-empty description="请上传图片文件" />
        </div>
      </el-card>

      <!-- 结果展示区域 -->
      <el-card
        v-if="workflowResult || workflowError"
        class="result-card"
        shadow="never"
      >
        <template #header>
          <span>执行结果</span>
        </template>

        <div v-if="workflowError" class="error-result">
          <el-alert
            :title="workflowError"
            type="error"
            :closable="false"
            show-icon
          />
        </div>

        <div v-if="workflowResult" class="success-result">
          <el-alert
            title="工作流执行成功"
            type="success"
            :closable="false"
            show-icon
            class="mb-4"
          />
          <el-descriptions :column="1" border>
            <el-descriptions-item label="任务ID">
              {{ workflowResult.task_id || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag
                :type="workflowResult.status === 'success' ? 'success' : 'info'"
              >
                {{ workflowResult.status }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>

          <div v-if="workflowResult.result" class="result-content mt-4">
            <div class="result-header">
              <h4>结果内容：</h4>
              <el-button
                type="primary"
                :icon="Download"
                :loading="downloading"
                @click="handleDownloadPDF"
              >
                下载 PDF 报告
              </el-button>
            </div>
            <el-scrollbar height="500px">
              <div ref="resultContentRef" class="result-display">
                <div v-if="extractedText" class="result-text">
                  <div v-html="formatText(extractedText)" />
                </div>
                <div v-else class="result-json">
                  <pre>{{ formatResult(workflowResult.result) }}</pre>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from "vue";
import { useArtTherapyWorkflow } from "./utils/hook";
import Play from "~icons/ep/video-play";
import Refresh from "~icons/ep/refresh";
import Download from "~icons/ep/download";
import Plus from "~icons/ep/plus";
import { message } from "@/utils/message";
import html2pdf from "html2pdf.js";
import { systemUploadFileApi } from "@/api/system/file";
import type {
  UploadFile,
  UploadProps,
  UploadRequestOptions
} from "element-plus";

defineOptions({
  name: "ArtTherapyWorkflow"
});

const {
  loading,
  uploadedFiles,
  workflowResult,
  workflowError,
  uploadImage,
  removeFile,
  clearFiles,
  runWorkflow,
  clearResult
} = useArtTherapyWorkflow();

const fileList = ref<UploadFile[]>([]);
const resultContentRef = ref<HTMLElement>();
const downloading = ref(false);

// 自定义上传请求
const handleUploadRequest = async (options: UploadRequestOptions) => {
  try {
    const formData = new FormData();
    formData.append("file", options.file);

    const response = await systemUploadFileApi.upload(formData, {
      onUploadProgress: (event: any) => {
        const progressEvt = event as any;
        progressEvt.percent =
          event.total > 0 ? (event.loaded / event.total) * 100 : 0;
        options.onProgress(progressEvt);
      }
    });

    if (response.code === 1000 && response.data && response.data.length > 0) {
      const uploadedFile = response.data[0];
      options.onSuccess(response);
      // 更新文件列表中的文件信息
      const file = fileList.value.find(f => f.uid === options.file.uid);
      if (file) {
        file.url = uploadedFile.access_url;
        file.pk = uploadedFile.pk;
        file.status = "success";
      }

      // 更新 uploadedFiles 状态，使按钮可用
      uploadedFiles.value.push({
        pk: uploadedFile.pk,
        filename: uploadedFile.filename,
        filesize: uploadedFile.filesize,
        filepath: uploadedFile.filepath || "",
        access_url: uploadedFile.access_url,
        file_type: uploadedFile.file_type || "image"
      });

      message("圖片上傳成功", { type: "success" });
    } else {
      options.onError(new Error("上傳失敗"));
      message("圖片上傳失敗", { type: "error" });
    }
  } catch (error) {
    options.onError(error as Error);
    message("圖片上傳失敗", { type: "error" });
  }
};

// 处理删除
const handleRemove = (file: UploadFile) => {
  if (file.pk) {
    removeFile(file.pk);
  }
  // 从 fileList 中移除
  const index = fileList.value.findIndex(f => f.uid === file.uid);
  if (index > -1) {
    fileList.value.splice(index, 1);
  }
  // 从 uploadedFiles 中移除
  const uploadedIndex = uploadedFiles.value.findIndex(f => f.pk === file.pk);
  if (uploadedIndex > -1) {
    uploadedFiles.value.splice(uploadedIndex, 1);
  }
};

// 上传前检查
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith("image/");
  const isLt10M = file.size / 1024 / 1024 < 10;

  if (!isImage) {
    message("只能上傳圖片文件", { type: "warning" });
    return false;
  }
  if (!isLt10M) {
    message("圖片大小不能超過 10MB", { type: "warning" });
    return false;
  }
  return true;
};

// 提取文本内容
const extractedText = computed(() => {
  if (!workflowResult.value?.result) return null;

  const result = workflowResult.value.result;

  // 尝试从 outputs.text 提取
  if (result?.outputs?.text) {
    return result.outputs.text;
  }

  // 尝试从 data.outputs.text 提取
  if (result?.data?.outputs?.text) {
    return result.data.outputs.text;
  }

  // 如果 result 本身就是字符串
  if (typeof result === "string") {
    return result;
  }

  return null;
});

// 格式化文本内容（处理 Markdown 和换行）
const formatText = (text: string) => {
  if (!text) return "";

  // 处理换行符
  let formatted = text.replace(/\\n/g, "\n");

  // 处理 Markdown 加粗 **text**
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // 处理 Markdown 标题
  formatted = formatted.replace(/^### (.*$)/gm, "<h3>$1</h3>");
  formatted = formatted.replace(/^## (.*$)/gm, "<h2>$1</h2>");
  formatted = formatted.replace(/^# (.*$)/gm, "<h1>$1</h1>");

  // 处理列表项
  formatted = formatted.replace(/^\d+\.\s+(.*$)/gm, "<li>$1</li>");

  // 将多个换行转换为段落
  formatted = formatted
    .split("\n\n")
    .map(para => {
      if (para.trim()) {
        // 如果包含列表项，包装在 ul 中
        if (para.includes("<li>")) {
          return `<ul>${para}</ul>`;
        }
        return `<p>${para}</p>`;
      }
      return "";
    })
    .join("");

  return formatted;
};

// 格式化結果顯示（用于 JSON）
const formatResult = (result: any) => {
  if (typeof result === "string") {
    return result;
  }
  return JSON.stringify(result, null, 2);
};

// 转换不支持的 CSS 颜色函数
const convertUnsupportedColors = (element: HTMLElement) => {
  const tempStyle = document.createElement("style");
  tempStyle.textContent = `
    * {
      color: #303133 !important;
      background-color: #ffffff !important;
      border-color: #e4e7ed !important;
    }
    h1, h2, h3 {
      color: #303133 !important;
    }
    strong {
      color: #303133 !important;
    }
  `;
  element.appendChild(tempStyle);

  const allElements = element.querySelectorAll("*");
  allElements.forEach(el => {
    const htmlEl = el as HTMLElement;
    if (htmlEl.style) {
      const computedStyle = window.getComputedStyle(htmlEl);
      if (computedStyle.color && computedStyle.color.includes("oklch")) {
        htmlEl.style.color = "#303133";
      }
      if (
        computedStyle.backgroundColor &&
        computedStyle.backgroundColor.includes("oklch")
      ) {
        htmlEl.style.backgroundColor = "#ffffff";
      }
    }
  });

  return element;
};

// 下载 PDF 报告
const handleDownloadPDF = async () => {
  if (!resultContentRef.value || !workflowResult.value?.result) {
    message("沒有可下載的內容", { type: "warning" });
    return;
  }

  try {
    downloading.value = true;

    const content = resultContentRef.value.cloneNode(true) as HTMLElement;
    const convertedContent = convertUnsupportedColors(content);

    const wrapper = document.createElement("div");
    wrapper.style.width = "210mm";
    wrapper.style.padding = "20px";
    wrapper.style.backgroundColor = "#ffffff";
    wrapper.style.color = "#303133";
    wrapper.appendChild(convertedContent);

    const opt = {
      margin: [10, 10, 10, 10],
      filename: `藝術治療報告_${new Date().getTime()}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: "#ffffff",
        removeContainer: true
      },
      jsPDF: {
        unit: "mm",
        format: "a4",
        orientation: "portrait"
      }
    };

    await html2pdf().set(opt).from(wrapper).save();

    message("PDF 報告下載成功", { type: "success" });
  } catch (error) {
    console.error("PDF 生成失敗:", error);
    message("PDF 報告下載失敗", { type: "error" });
  } finally {
    downloading.value = false;
  }
};

// 执行工作流
const handleRunWorkflow = () => {
  if (uploadedFiles.value.length === 0) {
    message("請至少上傳一張圖片", { type: "warning" });
    return;
  }

  runWorkflow();
};
</script>

<style lang="scss" scoped>
.art-therapy-workflow-container {
  padding: 20px;
}

.page-header {
  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;

    .page-title {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
    }

    .header-actions {
      display: flex;
      gap: 12px;
    }
  }
}

.workflow-content {
  margin-top: 20px;
}

.upload-card {
  .upload-tip {
    padding: 40px 0;
    text-align: center;
  }
}

.result-card {
  margin-top: 20px;
}

.result-content {
  .result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;

    h4 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
    }
  }
}

.result-display {
  .result-text {
    padding: 20px;
    font-size: 14px;
    line-height: 1.8;
    color: #303133;
    background-color: #fff;
    border: 1px solid #e4e7ed;
    border-radius: 4px;

    :deep(h1) {
      padding-bottom: 8px;
      margin: 20px 0 16px;
      font-size: 20px;
      font-weight: 600;
      color: #303133;
      border-bottom: 2px solid #409eff;
    }

    :deep(h2) {
      margin: 18px 0 12px;
      font-size: 18px;
      font-weight: 600;
      color: #303133;
    }

    :deep(h3) {
      margin: 16px 0 10px;
      font-size: 16px;
      font-weight: 600;
      color: #606266;
    }

    :deep(p) {
      margin: 12px 0;
      text-align: justify;
    }

    :deep(ul) {
      padding-left: 24px;
      margin: 12px 0;

      li {
        margin: 8px 0;
        list-style-type: disc;
      }
    }

    :deep(strong) {
      font-weight: 600;
      color: #303133;
    }
  }

  .result-json {
    padding: 16px;
    font-family: "Courier New", monospace;
    font-size: 14px;
    line-height: 1.6;
    word-wrap: break-word;
    white-space: pre-wrap;
    background-color: #f5f7fa;
    border-radius: 4px;

    pre {
      margin: 0;
    }
  }
}

.error-result {
  margin-bottom: 16px;
}

.success-result {
  .el-descriptions {
    margin-top: 16px;
  }
}
</style>
