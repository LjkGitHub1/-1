<template>
  <div v-loading="loading" class="knowledge-dataset-detail">
    <!-- 页面头部：标题 + 返回按钮 -->
    <page-header :title="datasetName" :show-back="true" @back="handleBack">
      <template #extra>
        <el-button type="primary" @click="handleRetrieve">
          <template #icon><icon-search /></template>
          执行检索
        </el-button>
        <el-button @click="handleEdit">
          <template #icon><icon-edit /></template>
          编辑
        </el-button>
        <el-popconfirm
          title="确定要删除该知识库吗？删除后将无法恢复！"
          @confirm="handleDelete"
        >
          <el-button danger>
            <template #icon><icon-delete /></template>
            删除
          </el-button>
        </el-popconfirm>
      </template>
    </page-header>

    <!-- 加载状态 -->
    <!-- 知识库基本信息 -->
    <div class="info-card mb-6">
      <el-card title="基本信息" bordered>
        <el-descriptions
          :column="3"
          :column-props="{ xs: 1, sm: 2, md: 3, lg: 3, xl: 3, xxl: 3 }"
        >
          <el-descriptions-item label="知识库ID">{{
            dataset.id || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="名称">{{
            dataset.name || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{
            dataset.description || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="提供商">{{
            dataset.provider || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="访问权限">{{
            formatPermission(dataset.permission)
          }}</el-descriptions-item>
          <el-descriptions-item label="索引技术">{{
            formatIndexingTechnique(dataset.indexing_technique)
          }}</el-descriptions-item>
          <el-descriptions-item label="关联应用数">{{
            dataset.app_count || 0
          }}</el-descriptions-item>
          <el-descriptions-item label="文档数量">{{
            dataset.document_count || 0
          }}</el-descriptions-item>
          <el-descriptions-item label="总字数">{{
            dataset.word_count || 0
          }}</el-descriptions-item>
          <el-descriptions-item label="嵌入模型">{{
            dataset.embedding_model || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="模型提供商">{{
            dataset.embedding_model_provider || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="嵌入可用">{{
            dataset.embedding_available ? "是" : "否"
          }}</el-descriptions-item>
          <el-descriptions-item label="创建人ID">{{
            dataset.created_by || "-"
          }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{
            formatTime(dataset.created_at)
          }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{
            formatTime(dataset.updated_at)
          }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <!-- 检索模型配置 -->
    <div v-if="dataset.retrieval_model_dict" class="retrieval-config-card mb-6">
      <el-card title="检索模型配置" bordered>
        <el-descriptions
          :column="2"
          :column-props="{ xs: 1, sm: 2, md: 2, lg: 2 }"
        >
          <el-descriptions-item label="搜索方法">{{
            formatSearchMethod(dataset.retrieval_model_dict.search_method)
          }}</el-descriptions-item>
          <el-descriptions-item label="是否启用重排序">{{
            dataset.retrieval_model_dict.reranking_enable ? "是" : "否"
          }}</el-descriptions-item>
          <el-descriptions-item
            v-if="dataset.retrieval_model_dict.reranking_mode"
            label="重排序提供商"
          >
            {{
              dataset.retrieval_model_dict.reranking_mode
                .reranking_provider_name || "-"
            }}
          </el-descriptions-item>
          <el-descriptions-item
            v-if="dataset.retrieval_model_dict.reranking_mode"
            label="重排序模型"
          >
            {{
              dataset.retrieval_model_dict.reranking_mode
                .reranking_model_name || "-"
            }}
          </el-descriptions-item>
          <el-descriptions-item label="返回结果数">{{
            dataset.retrieval_model_dict.top_k || 0
          }}</el-descriptions-item>
          <el-descriptions-item label="是否启用分数阈值">{{
            dataset.retrieval_model_dict.score_threshold_enabled ? "是" : "否"
          }}</el-descriptions-item>
          <el-descriptions-item
            v-if="dataset.retrieval_model_dict.score_threshold_enabled"
            label="分数阈值"
          >
            {{ dataset.retrieval_model_dict.score_threshold || 0 }}
          </el-descriptions-item>
          <el-descriptions-item
            v-if="dataset.retrieval_model_dict.weights"
            label="混合搜索权重"
          >
            {{ dataset.retrieval_model_dict.weights || 0 }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <!-- 标签信息 -->
    <div v-if="dataset.tags && dataset.tags.length" class="tags-card mb-6">
      <el-card title="关联标签" bordered>
        <el-tag
          v-for="(tag, index) in dataset.tags"
          :key="index"
          class="mb-2"
          color="blue"
          style="margin-right: 8px; margin-bottom: 8px"
        >
          {{ tag.name || `标签${index + 1}` }}
        </el-tag>
      </el-card>
    </div>

    <!-- 检索结果区域（始终展示卡片，结果为空时显示提示与操作） -->
    <div class="retrieval-result-card">
      <el-card title="检索结果" bordered>
        <div class="query-info mb-4">
          <span class="label">检索关键词：</span>
          <span class="value">{{ currentQuery || "(未检索)" }}</span>
        </div>

        <!-- 结果为空时显示提示和执行检索按钮 -->
        <div
          v-if="!retrievalResult.length"
          style="padding: 24px; color: rgb(0 0 0 / 45%); text-align: center"
        >
          <div style="margin-bottom: 12px">
            暂无检索结果。点击下方按钮进行检索。
          </div>
          <el-button type="primary" @click="handleRetrieve">
            <template #icon><icon-search /></template>
            执行检索
          </el-button>
        </div>

        <!-- 有结果时展示表格 -->
        <el-table
          v-else
          :columns="resultColumns"
          :data-source="retrievalResult"
          row-key="segment.id"
          pagination="{false}"
        >
          <template #bodyCell="{ record, column }">
            <template v-if="column.dataIndex === 'content'">
              <div class="content-cell">
                {{ record.segment.content }}
              </div>
            </template>
            <template v-if="column.dataIndex === 'document'">
              {{ record.segment.document.name || "-" }}
            </template>
            <template v-if="column.dataIndex === 'score'">
              {{ record.score.toFixed(4) }}
            </template>
          </template>
        </el-table>
      </el-card>
    </div>

    <!-- 检索弹窗 -->
    <retrieve-test-modal
      v-model:visible="retrieveModalVisible"
      :dataset-id="datasetId"
      :initial-retrieval-model="dataset.retrieval_model_dict"
      @confirm="handleRetrieveConfirm"
      @cancel="handleRetrieveCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, toRefs, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { message } from "@/utils/message";
import IconSearch from "~icons/ep/search";
import IconEdit from "~icons/ep/edit";
import IconDelete from "~icons/ep/delete";
import { knowledgeApi } from "@/api/knowledge";
import type {
  Dataset,
  RetrieveParams,
  RetrieveResponse,
  Segment
} from "../../../../types/knowledge";
import RetrieveTestModal from "./components/retrieve-test-modal.vue";

defineOptions({
  name: "KnowledgeManage" // 用于菜单自动匹配组件
});

/**
 * 时间格式化工具
 */
const formatTime = (timeStr: string | number) => {
  if (timeStr === null || timeStr === undefined || timeStr === "") return "-";
  // 支持 timestamp (秒) 或 ISO 字符串，两者兼容
  let date: Date;
  if (typeof timeStr === "number") {
    // 后端有时返回秒级时间戳
    date = new Date(timeStr * 1000);
  } else {
    // 尝试直接构造（支持 ISO 字符串 或 数字字符串）
    date = new Date(timeStr as string);
  }
  if (isNaN(date.getTime())) return "-";
  return date.toLocaleString();
};
// 路由实例
const router = useRouter();
const route = useRoute();

// 页面状态
const state = reactive({
  datasetId: route.params.id as string,
  dataset: {} as Dataset,
  datasetName: "知识库详情",
  loading: false,
  retrieveModalVisible: false,
  currentQuery: "",
  retrievalResult: [] as Array<{
    segment: Segment & { document: any };
    score: number;
  }>
});

const {
  datasetId,
  dataset,
  datasetName,
  loading,
  retrieveModalVisible,
  currentQuery,
  retrievalResult
} = toRefs(state);

// 监听路由参数变化
watch(
  () => route.params.id,
  newId => {
    if (newId) {
      datasetId.value = newId as string;
      fetchDatasetDetail();
    }
  },
  { immediate: true }
);

// 页面加载时获取数据
onMounted(() => {
  console.log("datasetId: ", datasetId.value);
  fetchDatasetDetail();
});

// 调试：监视弹窗可见性变化，帮助判断事件是否触发
import { watch as vueWatch } from "vue";
vueWatch(
  () => retrieveModalVisible.value,
  v => {
    console.log("retrieveModalVisible changed:", v);
  }
);

/**
 * 结果表格列配置
 */
const resultColumns = [
  {
    title: "内容片段",
    dataIndex: "content",
    key: "content",
    width: "50%"
  },
  {
    title: "所属文档",
    dataIndex: "document",
    key: "document",
    width: "20%"
  },
  {
    title: "匹配分数",
    dataIndex: "score",
    key: "score",
    width: "10%",
    sorter: (a: any, b: any) => a.score - b.score
  },
  {
    title: "位置",
    dataIndex: "position",
    key: "position",
    width: "10%",
    render: (text: any, record: any) => record.segment.position
  },
  {
    title: "字数",
    dataIndex: "wordCount",
    key: "wordCount",
    width: "10%",
    render: (text: any, record: any) => record.segment.word_count
  }
];

/**
 * 获取知识库详情
 */
const fetchDatasetDetail = async () => {
  // 当 route params 未提供 id 时，仍使用空字符串调用后端（后端可通过空 id 返回默认或列表）
  loading.value = true;
  try {
    // 使用空字符串替代 undefined/ null
    const idStr = datasetId.value ? String(datasetId.value) : null;
    const res: any = await knowledgeApi.getDatasetDetail(idStr);
    console.log("res: ", res);
    // 如果后端在 datasetId 为空时返回的是列表结构（{ data: Dataset[]... }），则取第一项作为详情展示
    if (res && Array.isArray(res.data)) {
      dataset.value = res.data[0] || ({} as Dataset);
    } else if (res && res.data && typeof res.data === "object") {
      // 有时接口会包一层 data
      dataset.value = res.data as Dataset;
    } else {
      // 直接当作对象处理（兼容不同后端）
      dataset.value = res as Dataset;
    }
    datasetName.value = (dataset.value && dataset.value.name) || "知识库详情";
  } catch (error) {
    message("获取知识库详情失败，请重试");
    console.error("Fetch dataset detail error:", error);
    handleBack(); // 加载失败返回列表页
  } finally {
    loading.value = false;
  }
};

/**
 * 返回列表页
 */
const handleBack = () => {
  router.push({ name: "DatasetList" });
};

/**
 * 编辑知识库
 */
const handleEdit = () => {
  // 跳转编辑页面或打开编辑弹窗（根据项目需求选择）
  router.push({ name: "DatasetList" });
  // 实际项目中可通过路由参数传递编辑状态
  // router.push({ name: 'DatasetForm', query: { id: datasetId.value, type: 'edit' } });
};

/**
 * 删除知识库
 */
const handleDelete = async () => {
  // 即使 datasetId 为空，也使用空字符串发起删除请求（后端可决定如何处理）
  loading.value = true;
  try {
    await knowledgeApi.deleteDataset(String(datasetId.value || ""));
    message("删除知识库成功");
    handleBack();
  } catch (error) {
    message("删除知识库失败，请重试");
    console.error("Delete dataset error:", error);
  } finally {
    loading.value = false;
  }
};

/**
 * 打开检索弹窗
 */
const handleRetrieve = () => {
  console.log("handleRetrieve");
  retrieveModalVisible.value = true;
};

/**
 * 检索确认
 */
const handleRetrieveConfirm = async (params: RetrieveParams) => {
  loading.value = true;
  try {
    // 使用空字符串代替未定义 id，确保始终发起请求
    const idStr = datasetId.value ? String(datasetId.value) : "";

    const res: RetrieveResponse = await knowledgeApi.retrieveFromDataset(
      idStr,
      params
    );
    currentQuery.value = params.query;
    retrievalResult.value = res.records;
    retrieveModalVisible.value = false;
  } catch (error) {
    message("检索失败，请重试");
    console.error("Retrieve dataset error:", error);
  } finally {
    loading.value = false;
  }
};

/**
 * 检索取消
 */
const handleRetrieveCancel = () => {
  console.log("handleRetrieveCancel");
  retrieveModalVisible.value = false;
};

/**
 * 格式化权限类型
 */
const formatPermission = (permission?: string) => {
  const map: Record<string, string> = {
    only_me: "仅自己可见",
    all_team_members: "团队成员可见",
    partial_members: "指定成员可见"
  };
  return map[permission || ""] || "-";
};

/**
 * 格式化索引技术
 */
const formatIndexingTechnique = (technique?: string) => {
  const map: Record<string, string> = {
    high_quality: "高质量索引",
    economy: "经济型索引"
  };
  return map[technique || ""] || "-";
};

/**
 * 格式化搜索方法
 */
const formatSearchMethod = (method?: string) => {
  const map: Record<string, string> = {
    hybrid_search: "混合搜索",
    semantic_search: "语义搜索",
    full_text_search: "全文搜索",
    keyword_search: "关键词搜索"
  };
  return map[method || ""] || "-";
};
</script>

<style scoped lang="less">
.knowledge-dataset-detail {
  padding: 16px;
  background: #fff;
  min-height: calc(100vh - 120px);

  .info-card,
  .retrieval-config-card,
  .tags-card,
  .retrieval-result-card {
    margin-bottom: 16px;
  }

  .query-info {
    margin-bottom: 12px;
    .label {
      font-weight: 500;
      margin-right: 8px;
    }
    .value {
      color: #1890ff;
    }
  }

  .content-cell {
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 120px;
    overflow-y: auto;
  }
}
</style>
