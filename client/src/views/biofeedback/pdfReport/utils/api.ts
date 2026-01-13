import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class PdfReportApi extends BaseApi {
  getList = (params?: any) => this.request<BaseResult>("get", params, {}, "");
  getDetail = (pk: number | string) =>
    this.request<BaseResult>("get", {}, {}, `/${pk}`);
  delete = (pk: number | string) =>
    this.request<BaseResult>("delete", {}, {}, `/${pk}`);
  // 自定义操作：下载报告
  download = (pk: number | string) =>
    this.request<BaseResult>("get", {}, {}, `/${pk}/download`);
}

const pdfReportApi = new PdfReportApi("/api/biofeedback/pdf-report");
export { pdfReportApi };
