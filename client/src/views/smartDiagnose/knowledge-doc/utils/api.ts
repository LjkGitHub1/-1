import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class KnowledgeDocApi extends BaseApi {
  // 无自定义接口，默认CRUD
  push = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/push`
    );
  };
}

const knowledgeDocApi = new KnowledgeDocApi("/api/smartDiagnose/knowledge-doc");
export { knowledgeDocApi };
