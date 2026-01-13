import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class PatientApi extends BaseApi {
  // 基础CRUD接口
  getList = (params?: any) => this.request<BaseResult>("get", params, {}, "");
  getDetail = (pk: number | string) =>
    this.request<BaseResult>("get", {}, {}, `/${pk}`);
  // 删除
  delete = (pk: number | string) =>
    this.request<BaseResult>("delete", {}, {}, `/${pk}`);
}

const patientApi = new PatientApi("/api/biofeedback/patient");
export { patientApi };
