<template>
  <el-dialog
    v-model:visible="dialogVisible"
    title="知识库检索测试"
    :destroy-on-close="true"
    width="800px"
  >
    <el-form
      ref="formRef"
      :model="formValues"
      :rules="formRules"
      label-position="top"
    >
      <!-- 检索关键词 -->
      <el-form-item label="检索关键词" prop="query">
        <el-input
          v-model="formValues.query"
          maxlength="500"
          clearable
          placeholder="请输入检索关键词"
        />
      </el-form-item>

      <!-- 检索模型配置（折叠面板） -->
      <el-collapse v-model="activeKey">
        <el-collapse-item title="检索模型配置" name="retrievalModel">
          <div class="retrieval-model-form">
            <el-form-item label="搜索方法" prop="retrieval_model.search_method">
              <el-select
                v-model="formValues.retrieval_model.search_method"
                placeholder="请选择搜索方法"
              >
                <el-option label="混合搜索" value="hybrid_search" />
                <el-option label="语义搜索" value="semantic_search" />
                <el-option label="全文搜索" value="full_text_search" />
                <el-option label="关键词搜索" value="keyword_search" />
              </el-select>
            </el-form-item>

            <el-form-item
              label="是否启用重排序"
              prop="retrieval_model.reranking_enable"
            >
              <el-select
                v-model="formValues.retrieval_model.reranking_enable"
                placeholder="请选择"
              >
                <el-option :label="'是'" :value="true" />
                <el-option :label="'否'" :value="false" />
              </el-select>
            </el-form-item>

            <template v-if="formValues.retrieval_model.reranking_enable">
              <el-form-item
                label="重排序提供商"
                prop="retrieval_model.reranking_mode.reranking_provider_name"
              >
                <el-input
                  v-model="
                    formValues.retrieval_model.reranking_mode
                      .reranking_provider_name
                  "
                  placeholder="请输入重排序提供商"
                />
              </el-form-item>

              <el-form-item
                label="重排序模型"
                prop="retrieval_model.reranking_mode.reranking_model_name"
              >
                <el-input
                  v-model="
                    formValues.retrieval_model.reranking_mode
                      .reranking_model_name
                  "
                  placeholder="请输入重排序模型"
                />
              </el-form-item>
            </template>

            <el-form-item label="返回结果数" prop="retrieval_model.top_k">
              <el-input-number
                v-model="formValues.retrieval_model.top_k"
                :min="1"
                :max="100"
              />
            </el-form-item>

            <el-form-item
              label="是否启用分数阈值"
              prop="retrieval_model.score_threshold_enabled"
            >
              <el-select
                v-model="formValues.retrieval_model.score_threshold_enabled"
                placeholder="请选择"
              >
                <el-option :label="'是'" :value="true" />
                <el-option :label="'否'" :value="false" />
              </el-select>
            </el-form-item>

            <template v-if="formValues.retrieval_model.score_threshold_enabled">
              <el-form-item
                label="分数阈值"
                prop="retrieval_model.score_threshold"
              >
                <el-input-number
                  v-model="formValues.retrieval_model.score_threshold"
                  :min="0"
                  :max="1"
                  :step="0.0001"
                />
              </el-form-item>
            </template>

            <template
              v-if="
                formValues.retrieval_model.search_method === 'hybrid_search'
              "
            >
              <el-form-item
                label="混合搜索权重（语义搜索占比）"
                prop="retrieval_model.weights"
              >
                <el-input-number
                  v-model="formValues.retrieval_model.weights"
                  :min="0"
                  :max="1"
                  :step="0.01"
                />
              </el-form-item>
            </template>

            <el-form-item label="是否启用元数据过滤">
              <el-select
                v-model="enableMetadataFilter"
                placeholder="请选择"
                @change="handleMetadataFilterChange"
              >
                <el-option :label="'是'" :value="true" />
                <el-option :label="'否'" :value="false" />
              </el-select>
            </el-form-item>

            <template
              v-if="formValues.retrieval_model.metadata_filtering_conditions"
            >
              <el-form-item
                label="逻辑运算符"
                prop="retrieval_model.metadata_filtering_conditions.logical_operator"
              >
                <el-select
                  v-model="
                    formValues.retrieval_model.metadata_filtering_conditions
                      .logical_operator
                  "
                  placeholder="请选择逻辑运算符"
                >
                  <el-option label="且" value="and" />
                  <el-option label="或" value="or" />
                </el-select>
              </el-form-item>

              <div class="metadata-conditions">
                <el-form-item
                  label="条件1：字段名"
                  prop="retrieval_model.metadata_filtering_conditions.conditions[0].name"
                >
                  <el-input
                    v-model="
                      formValues.retrieval_model.metadata_filtering_conditions
                        .conditions[0].name
                    "
                    placeholder="请输入元数据字段名（如：category）"
                  />
                </el-form-item>

                <el-form-item
                  label="条件1：运算符"
                  prop="retrieval_model.metadata_filtering_conditions.conditions[0].comparison_operator"
                >
                  <el-select
                    v-model="
                      formValues.retrieval_model.metadata_filtering_conditions
                        .conditions[0].comparison_operator
                    "
                    placeholder="请选择运算符"
                  >
                    <el-option label="等于" value="eq" />
                    <el-option label="不等于" value="ne" />
                    <el-option label="大于" value="gt" />
                    <el-option label="大于等于" value="ge" />
                    <el-option label="小于" value="lt" />
                    <el-option label="小于等于" value="le" />
                    <el-option label="包含" value="contains" />
                  </el-select>
                </el-form-item>

                <el-form-item
                  label="条件1：值"
                  prop="retrieval_model.metadata_filtering_conditions.conditions[0].value"
                >
                  <el-input
                    v-model="
                      formValues.retrieval_model.metadata_filtering_conditions
                        .conditions[0].value
                    "
                    placeholder="请输入比较值"
                  />
                </el-form-item>
              </div>
            </template>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-form>

    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" :loading="confirmLoading" @click="handleOk"
        >确定</el-button
      >
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import {
  ref,
  reactive,
  toRefs,
  watch,
  onBeforeMount,
  toRef,
  computed
} from "vue";
import type {
  RetrieveParams,
  RetrievalModel
} from "../../../../../types/knowledge";

// 组件props定义
const props = defineProps<{
  visible: boolean;
  datasetId: string; // 知识库ID（用于后续请求，当前暂存）
  initialRetrievalModel?: RetrievalModel; // 初始检索模型配置（从详情页传入）
}>();

onBeforeMount(() => {
  console.log("onBeforeMount", props.visible);
});

// 组件事件触发
const emit = defineEmits(["confirm", "cancel", "update:visible"] as const);

// 表单实例引用（用于校验）
const formRef = ref<any>(null);

// 组件内部状态
const state = reactive({
  // 表单值（与RetrieveParams类型一致）
  formValues: {
    query: "",
    retrieval_model: {
      search_method: "hybrid_search" as
        | "hybrid_search"
        | "semantic_search"
        | "full_text_search"
        | "keyword_search",
      reranking_enable: false,
      reranking_mode: {
        reranking_provider_name: "",
        reranking_model_name: ""
      } as any | null,
      top_k: 10,
      score_threshold_enabled: false,
      score_threshold: 0,
      weights: 0.5,
      metadata_filtering_conditions: undefined as any
    } as RetrievalModel
  } as RetrieveParams,

  confirmLoading: false, // 提交加载状态
  activeKey: ["retrievalModel"] // 折叠面板默认激活项
});

const { formValues, confirmLoading, activeKey } = toRefs(state);

// 将父传入的 visible prop 代理为可双向绑定的值，便于与 el-dialog 的 v-model:visible 配合使用
const visibleProp = toRef(props, "visible");
const dialogVisible = computed<boolean>({
  get: () => !!visibleProp.value,
  set: val => {
    emit("update:visible", val);
  }
});

// 表单校验规则（Element Plus 形式）
const formRules = reactive({
  query: [{ required: true, message: "请输入检索关键词", trigger: "blur" }],
  "retrieval_model.search_method": [
    { required: true, message: "请选择搜索方法", trigger: "change" }
  ],
  "retrieval_model.top_k": [
    { required: true, message: "请输入返回结果数", trigger: "blur" },
    {
      type: "number",
      min: 1,
      max: 100,
      message: "返回结果数需在1-100之间",
      trigger: "blur"
    }
  ]
}) as any;

// 监听初始检索模型配置变化（从详情页传入时初始化表单）
watch(
  () => props.initialRetrievalModel,
  newVal => {
    if (newVal) {
      // 深拷贝初始配置，避免修改原数据
      formValues.value.retrieval_model = JSON.parse(JSON.stringify(newVal));

      // 补全必要的默认值
      if (
        formValues.value.retrieval_model.reranking_enable &&
        !formValues.value.retrieval_model.reranking_mode
      ) {
        formValues.value.retrieval_model.reranking_mode = {
          reranking_provider_name: "",
          reranking_model_name: ""
        } as any;
      }

      if (formValues.value.retrieval_model.metadata_filtering_conditions) {
        if (
          !formValues.value.retrieval_model.metadata_filtering_conditions
            .conditions
        ) {
          formValues.value.retrieval_model.metadata_filtering_conditions = {
            logical_operator: "and",
            conditions: [{ name: "", comparison_operator: "eq", value: "" }]
          } as any;
        }
      }
    }
  },
  { immediate: true, deep: true }
);

const enableMetadataFilter = ref(
  !!formValues.value.retrieval_model.metadata_filtering_conditions
);

/**
 * 元数据过滤启用状态变化处理
 */
const handleMetadataFilterChange = (value: boolean) => {
  if (value) {
    // 启用：初始化过滤条件结构
    formValues.value.retrieval_model.metadata_filtering_conditions = {
      logical_operator: "and",
      conditions: [{ name: "", comparison_operator: "eq", value: "" }]
    } as any;
  } else {
    // 禁用：清空过滤条件
    formValues.value.retrieval_model.metadata_filtering_conditions =
      undefined as any;
  }
  enableMetadataFilter.value = value;
};

/**
 * 确认检索（弹窗确定按钮）
 */
const handleOk = async () => {
  try {
    // 表单校验
    await formRef.value?.validate();
    state.confirmLoading = true;

    // 处理重排序模式（未启用时设为null，符合接口要求）
    if (!formValues.value.retrieval_model.reranking_enable) {
      formValues.value.retrieval_model.reranking_mode = null as any;
    }

    // 触发父组件的确认事件，传递检索参数
    emit("confirm", { ...formValues.value });
  } catch (error) {
    console.error("检索表单校验失败：", error);
    // 校验失败不关闭弹窗，保留用户输入
  } finally {
    state.confirmLoading = false;
  }
};

/**
 * 取消检索（弹窗取消按钮）
 */
const handleCancel = () => {
  // 主动通知父组件关闭弹窗并触发取消事件
  emit("update:visible", false);
  emit("cancel");
  // 重置表单（避免下次打开时残留上次输入）
  formRef.value?.resetFields?.();
};
</script>

<style scoped lang="less">
.retrieval-model-form {
  padding: 8px 0;

  .el-form-item {
    margin-bottom: 16px;
  }
}

.metadata-conditions {
  border: 1px dashed #d9d9d9;
  padding: 16px;
  border-radius: 4px;
  margin-top: 8px;

  .el-form-item {
    margin-bottom: 12px;
  }
}
</style>
