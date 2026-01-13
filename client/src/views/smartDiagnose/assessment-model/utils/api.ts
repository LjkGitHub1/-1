import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class AssessmentModelApi extends BaseApi {
  train = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/train`
    );
  };
}

const assessmentModelApi = new AssessmentModelApi(
  "/api/smartDiagnose/assessment-model"
);

export { assessmentModelApi };
