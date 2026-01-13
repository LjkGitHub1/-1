import { BaseApi } from "@/api/base";
import type {
  GetDatasetListParams,
  DatasetListResponse,
  CreateDatasetParams,
  Dataset,
  RetrieveParams,
  RetrieveResponse,
  ErrorResponse
} from "../../types/knowledge";

/** 知识库API类 */
export class KnowledgeApi extends BaseApi {
  /** 基础路径 */
  private baseUrl = "http://localhost/v1/datasets";

  /**
   * 获取知识库列表（支持分页和过滤）
   * @param params - 请求参数
   */
  getDatasetList(params: GetDatasetListParams): Promise<DatasetListResponse> {
    return this.request<DatasetListResponse>(
      "get",
      params,
      {},
      `${this.baseUrl}`,
      this.buildAuthConfig()
    );
  }

  /**
   * 创建空知识库
   * @param data - 创建参数
   */
  createDataset(data: CreateDatasetParams): Promise<Dataset | ErrorResponse> {
    return this.request<Dataset | ErrorResponse>(
      "post",
      {},
      data,
      `${this.baseUrl}`,
      this.buildAuthConfig()
    );
  }

  /**
   * 获取知识库详情
   * @param datasetId - 知识库ID
   */
  // datasetId 可为空：当为空时请调用基础列表路径（不拼接 '/<id>'）
  getDatasetDetail(datasetId?: string | null): Promise<Dataset> {
    const url = datasetId ? `${this.baseUrl}/${datasetId}` : this.baseUrl;
    console.log("url: ", url);
    return this.request<Dataset>("get", {}, {}, url, this.buildAuthConfig());
  }

  /**
   * 删除知识库
   * @param datasetId - 知识库ID
   */
  deleteDataset(datasetId: string): Promise<void> {
    return this.request<void>(
      "delete",
      {},
      {},
      `${this.baseUrl}/${datasetId}`,
      this.buildAuthConfig()
    );
  }

  /**
   * 从知识库检索内容块
   * @param datasetId - 知识库ID
   * @param data - 检索参数
   */
  retrieveFromDataset(
    datasetId: string,
    data: RetrieveParams
  ): Promise<RetrieveResponse> {
    return this.request<RetrieveResponse>(
      "post",
      {},
      data,
      `${this.baseUrl}/${datasetId}/retrieve`,
      this.buildAuthConfig()
    );
  }

  /**
   * 构建鉴权请求头（Bearer Token）
   */
  private getAuthHeader(): Record<string, string> {
    // 从全局状态获取API-Key（实际项目中需从安全存储获取）
    const apiKey = this.getApiKey();
    return {
      Authorization: `Bearer ${apiKey}`
    };
  }

  /**
   * 构建请求配置并确保在请求前设置 Authorization（以避免被全局拦截器自动覆盖）
   */
  private buildAuthConfig() {
    const header = this.getAuthHeader();
    // 一些后端可能要求不同的 header 名称（比如 X-API-Key / Api-Key / Authorization: Token）
    // 我们在此处同时注入常见的几种变体以提高兼容性。
    // 仅发送标准的 Authorization 头，避免触发预检请求中的自定义头名问题（如 X-API-Key）
    // 如果后端确实需要其他自定义头（X-API-Key / Api-Key），需要在后端 CORS 设置中允许这些头。
    return {
      headers: header,
      beforeRequestCallback: (config: any) => {
        config.headers = {
          ...(config.headers || {}),
          ...header
        };
        return config;
      }
    } as any;
  }

  /**
   * 获取API-Key（实际项目中需替换为真实的获取逻辑）
   */
  private getApiKey(): string {
    // 示例：从localStorage获取（生产环境建议从后端接口动态获取）
    // return localStorage.getItem("apiKey") || "dataset-IASJsKh5T9W38Sdj5kN6TCXO";
    return "dataset-IASJsKh5T9W38Sdj5kN6TCXO";
  }
}

/** 实例化API对象 */
export const knowledgeApi = new KnowledgeApi("http://localhost/v1/datasets");
