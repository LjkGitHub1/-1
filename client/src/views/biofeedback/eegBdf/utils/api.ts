import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class EegBdfApi extends BaseApi {
  getList = (params?: any) => this.request<BaseResult>("get", params, {}, "");
  getDetail = (pk: number | string) =>
    this.request<BaseResult>("get", {}, {}, `/${pk}`);
  delete = (pk: number | string) =>
    this.request<BaseResult>("delete", {}, {}, `/${pk}`);
  // 自定义操作：标记为已分析
  analyze = (pk: number | string) =>
    this.request<BaseResult>("post", {}, {}, `/${pk}/analyze`);
}

const eegBdfApi = new EegBdfApi("/api/biofeedback/eeg-bdf");
export { eegBdfApi };
