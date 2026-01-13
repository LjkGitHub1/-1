/** 基础响应格式 */
export interface BaseResponse {
  code?: number;
  message?: string;
}

/** 基础API类（项目已存在，此处补充必要方法） */
export class BaseApi {
  protected request: <T>(
    method: "get" | "post" | "put" | "delete",
    url: string,
    data?: any,
    options?: any
  ) => Promise<T>;

  // 以下方法为项目已有实现，此处仅作类型声明
  get<T>(url: string, options?: any): Promise<T> {
    return this.request("get", url, null, options);
  }

  post<T>(url: string, data?: any, options?: any): Promise<T> {
    return this.request("post", url, data, options);
  }

  delete<T>(url: string, options?: any): Promise<T> {
    return this.request("delete", url, null, options);
  }
}
