import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class PersonalizedAssessmentApi extends BaseApi {
  refreshPlan = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/refresh_plan`
    );
  };

  generateReport = (payload: Record<string, any>) => {
    return this.request<BaseResult>(
      "post",
      payload,
      {},
      `${this.baseApi}/generate_report`
    );
  };
}

const personalizedAssessmentApi = new PersonalizedAssessmentApi(
  "/api/smartDiagnose/personalized-assessment"
);

export { personalizedAssessmentApi };
