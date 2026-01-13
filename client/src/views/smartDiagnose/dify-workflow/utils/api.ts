import { BaseApi } from "@/api/base";
import type { DetailResult } from "@/api/types";

// Dify 工作流调用请求参数
interface DifyWorkflowRequest {
  file_ids: number[]; // 选中的文件ID列表
  inputs?: Record<string, any>; // 工作流的输入参数（可选）
}

// Dify 工作流响应结果
interface DifyWorkflowResponse {
  task_id: string;
  status: string;
  result?: any;
  error?: string;
}

class DifyWorkflowApi extends BaseApi {
  /**
   * 调用 Dify 工作流
   * @param data 包含文件ID列表和工作流输入参数
   */
  runWorkflow = (data: DifyWorkflowRequest) => {
    // 使用完整的 action 路径，参考 chat-qa 的实现方式
    const runApi = new BaseApi("/api/smartDiagnose/dify-workflow/run");
    return runApi.request<DetailResult<DifyWorkflowResponse>>(
      "post",
      {},
      data,
      `${runApi.baseApi}`,
      {
        timeout: 300000 // 增加超时时间到 5 分钟（300秒）
      }
    );
  };

  /**
   * 获取工作流执行状态
   * @param taskId 任务ID
   */
  getWorkflowStatus = (taskId: string) => {
    // 使用完整的 action 路径
    const statusApi = new BaseApi(
      `/api/smartDiagnose/dify-workflow/status/${taskId}`
    );
    return statusApi.request<DetailResult<DifyWorkflowResponse>>(
      "get",
      {},
      {},
      `${statusApi.baseApi}`
    );
  };
}

export const difyWorkflowApi = new DifyWorkflowApi(
  "/api/smartDiagnose/dify-workflow"
);
export type { DifyWorkflowRequest, DifyWorkflowResponse };
