import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class ModelConfigApi extends BaseApi {
  // 继承BaseApi，无需额外自定义接口（默认CRUD）
  push = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/push`
    );
  };
}

// 按文档规范：基础接口地址与后端config.py的URLPATTERNS对应
const modelConfigApi = new ModelConfigApi("/api/smartDiagnose/model-config");
export { modelConfigApi };
