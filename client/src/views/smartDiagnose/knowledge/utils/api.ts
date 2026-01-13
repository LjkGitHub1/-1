import { BaseApi } from "@/api/base";
import type { BaseResult, DetailResult } from "@/api/types";

// 知识库列表请求参数类型
interface DatasetListParams {
  keyword?: string;
  tag_ids?: string[];
  page?: number;
  limit?: number;
  include_all?: boolean;
}

// 知识库列表响应类型
interface DatasetListResponse {
  data: Dataset[];
  has_more: boolean;
  limit: number;
  total: number;
  page: number;
}

// 知识库详情类型
interface Dataset {
  id: string;
  name: string;
  description?: string;
  provider: string;
  permission: string;
  data_source_type?: string;
  indexing_technique?: string;
  app_count: number;
  document_count: number;
  word_count: number;
  created_by: string;
  created_at: number;
  updated_by: string;
  updated_at: number;
  embedding_model?: string;
  embedding_model_provider?: string;
  embedding_available?: boolean;
  retrieval_model_dict?: RetrievalModel;
  tags?: Array<Record<string, any>>;
  doc_form?: string;
}

// 创建知识库请求参数类型
interface CreateDatasetParams {
  name: string;
  description?: string;
  indexing_technique: "high_quality" | "economy";
  permission: "only_me" | "all_team_members" | "partial_members";
  provider: "vendor" | "external";
  external_knowledge_api_id?: string;
  external_knowledge_id?: string;
  embedding_model: string;
  embedding_model_provider: string;
  retrieval_model?: RetrievalModel;
}

// 检索请求参数类型
interface RetrieveParams {
  query: string;
  retrieval_model: RetrievalModel & {
    metadata_filtering_conditions?: {
      logical_operator: "and" | "or";
      conditions: Array<{
        name: string;
        comparison_operator: string;
        value?: string | number;
      }>;
    };
  };
}

// 检索响应类型
// interface RetrieveResponse {
//   query: {
//     content: string;
//   };
//   records: Array<{
//     segment: Segment & {
//       document: {
//         id: string;
//         data_source_type: string;
//         name: string;
//       };
//     };
//     score: number;
//   }>;
// }

// 检索模型配置类型
interface RetrievalModel {
  search_method:
    | "hybrid_search"
    | "semantic_search"
    | "full_text_search"
    | "keyword_search";
  reranking_enable: boolean;
  reranking_mode?: {
    reranking_provider_name: string;
    reranking_model_name: string;
  };
  top_k: number;
  score_threshold_enabled: boolean;
  score_threshold?: number;
  weights?: number;
}

// 片段类型
// interface Segment {
//   id: string;
//   position: number;
//   document_id: string;
//   content: string;
//   answer?: string;
//   word_count: number;
//   tokens: number;
//   keywords?: string[];
//   index_node_id: string;
//   index_node_hash: string;
//   hit_count: number;
//   enabled: boolean;
//   disabled_at?: number;
//   disabled_by?: string;
//   status: string;
//   created_by: string;
//   created_at: number;
//   indexing_at: number;
//   completed_at: number;
//   error?: string;
//   stopped_at?: number;
// }

class KnowledgeApi extends BaseApi {
  // 获取知识库列表
  getList = (params: DatasetListParams) => {
    return this.request<
      { code: number; message: string } & DatasetListResponse
    >("get", { ...params }, {}, `http://localhost/v1/datasets`);
  };

  // 创建空知识库
  create = (data: CreateDatasetParams) => {
    return this.request<DetailResult>(
      "post",
      {},
      data,
      `http://localhost/v1/datasets`
    );
  };

  // 获取知识库详情
  getDetail = (datasetId: string) => {
    return this.request<DetailResult>(
      "get",
      {},
      {},
      `http://localhost/v1/datasets/${datasetId}`
    );
  };

  // 删除知识库
  // 删除知识库
  deleteDataset = (datasetId: string) => {
    return this.request<BaseResult>(
      "delete",
      {},
      {},
      `http://localhost/v1/datasets/${datasetId}`
    );
  };

  // 检索知识库内容
  retrieveDataset = (datasetId: string, data: RetrieveParams) => {
    return this.request<DetailResult>(
      "post",
      {},
      data,
      `http://localhost/v1/datasets/${datasetId}/retrieve`
    );
  };
}

const knowledgeApi = new KnowledgeApi("http://localhost/v1"); // 基础路径根据实际项目调整
export { knowledgeApi };
export type { Dataset, DatasetListParams, CreateDatasetParams, RetrieveParams };
