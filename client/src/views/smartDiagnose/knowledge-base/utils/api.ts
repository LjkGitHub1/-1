import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class KnowledgeBaseApi extends BaseApi {
  // 自定义同步文档数量接口（对应后端action）
  syncDocCount = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/sync_doc_count`
    );
  };
}

const knowledgeBaseApi = new KnowledgeBaseApi(
  "/api/smartDiagnose/knowledge-base"
);
export { knowledgeBaseApi };
