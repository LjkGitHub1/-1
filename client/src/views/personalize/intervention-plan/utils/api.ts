import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class InterventionPlanApi extends BaseApi {
  // 启动方案接口
  start = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/start`
    );
  };
}

const interventionPlanApi = new InterventionPlanApi(
  "/api/personalize/intervention_plan"
);
export { interventionPlanApi };
