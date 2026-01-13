import type { BaseResponse } from "./base";

/** 检索模型配置 */
export interface RetrievalModel {
  /** 搜索方法 */
  search_method:
    | "hybrid_search"
    | "semantic_search"
    | "full_text_search"
    | "keyword_search";
  /** 是否启用重新排序 */
  reranking_enable: boolean;
  /** 重新排序配置 */
  reranking_mode?: {
    reranking_provider_name: string;
    reranking_model_name: string;
  } | null;
  /** 返回结果数量 */
  top_k: number;
  /** 是否启用分数阈值 */
  score_threshold_enabled: boolean;
  /** 分数阈值 */
  score_threshold?: number | null;
  /** 混合搜索权重 */
  weights?: number | null;
  /** 元数据过滤条件（仅检索时使用） */
  metadata_filtering_conditions?: {
    logical_operator: "and" | "or";
    conditions: Array<{
      name: string;
      comparison_operator: string;
      value?: string | number | null;
    }>;
  };
}

/** 知识库信息 */
export interface Dataset {
  id: string; // UUID
  name: string;
  description?: string | null;
  provider: string;
  permission: string;
  data_source_type?: string | null;
  indexing_technique?: string | null;
  app_count: number;
  document_count: number;
  word_count: number;
  created_by: string; // UUID
  created_at: number; // 时间戳
  updated_by: string; // UUID
  updated_at: number; // 时间戳
  embedding_model?: string | null;
  embedding_model_provider?: string | null;
  embedding_available?: boolean | null;
  /** 检索模型配置（详情接口返回） */
  retrieval_model_dict?: RetrievalModel;
  /** 标签列表（详情接口返回） */
  tags?: Array<Record<string, any>>;
  /** 文档表单（详情接口返回） */
  doc_form?: string | null;
}

/** 知识库列表请求参数 */
export interface GetDatasetListParams {
  /** 搜索关键词 */
  keyword?: string;
  /** 标签ID列表 */
  tag_ids?: string[];
  /** 页码（默认1） */
  page?: number;
  /** 每页数量（默认20，最大100） */
  limit?: number;
  /** 是否包含所有数据集（仅所有者有效） */
  include_all?: boolean;
}

/** 知识库列表响应 */
export interface DatasetListResponse extends BaseResponse {
  data: Dataset[];
  has_more: boolean;
  limit: number;
  total: number;
  page: number;
}

/** 创建知识库请求参数 */
export interface CreateDatasetParams {
  /** 知识库名称（必填） */
  name: string;
  /** 描述 */
  description?: string;
  /** 索引技术（必填） */
  indexing_technique: "high_quality" | "economy";
  /** 访问权限（必填） */
  permission: "only_me" | "all_team_members" | "partial_members";
  /** 提供商（必填） */
  provider: "vendor" | "external";
  /** 外部知识API ID（provider为external时必填） */
  external_knowledge_api_id?: string;
  /** 外部知识ID（provider为external时必填） */
  external_knowledge_id?: string;
  /** 嵌入模型名称（必填） */
  embedding_model: string;
  /** 嵌入模型提供商（必填） */
  embedding_model_provider: string;
  /** 检索模型配置 */
  retrieval_model?: RetrievalModel;
}

/** 检索请求参数 */
export interface RetrieveParams {
  /** 搜索查询字符串（必填） */
  query: string;
  /** 检索模型配置（必填） */
  retrieval_model: RetrievalModel;
}

/** 检索结果片段 */
export interface Segment {
  id: string; // UUID
  position: number;
  document_id: string; // UUID
  content: string;
  answer?: string | null;
  word_count: number;
  tokens: number;
  keywords?: string[];
  index_node_id: string;
  index_node_hash: string;
  hit_count: number;
  enabled: boolean;
  disabled_at?: number | null;
  disabled_by?: string | null;
  status: string;
  created_by: string; // UUID
  created_at: number; // 时间戳
  indexing_at: number; // 时间戳
  completed_at: number; // 时间戳
  error?: string | null;
  stopped_at?: number | null;
  /** 关联文档信息 */
  document: {
    id: string; // UUID
    data_source_type: string;
    name: string;
  };
}

/** 检索响应结果 */
export interface RetrieveResponse extends BaseResponse {
  query: {
    content: string;
  };
  records: Array<{
    segment: Segment;
    score: number;
  }>;
}

/** 错误响应 */
export interface ErrorResponse {
  code: string;
  message: string;
  status: number;
}
