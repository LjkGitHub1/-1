import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class AssessmentReportApi extends BaseApi {
  // 归档报告接口
  archive = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/archive`
    );
  };
}

// 基础接口地址（与后端config.py的URLPATTERNS对应）
const assessmentReportApi = new AssessmentReportApi(
  "/api/personalize/assessment_report"
);
export { assessmentReportApi };
