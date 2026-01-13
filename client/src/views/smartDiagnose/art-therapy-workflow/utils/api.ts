import { BaseApi } from "@/api/base";
import type { DetailResult } from "@/api/types";

// 艺术治疗工作流调用请求参数
interface ArtTherapyWorkflowRequest {
  file_ids: number[]; // 上传的图片文件ID列表
  inputs?: Record<string, any>; // 工作流的输入参数（可选）
}

// 艺术治疗工作流响应结果
interface ArtTherapyWorkflowResponse {
  task_id: string;
  status: string;
  result?: any;
  error?: string;
}

class ArtTherapyWorkflowApi extends BaseApi {
  /**
   * 调用艺术治疗工作流
   * @param data 包含文件ID列表和工作流输入参数
   */
  runWorkflow = (data: ArtTherapyWorkflowRequest) => {
    const runApi = new BaseApi("/api/smartDiagnose/art-therapy-workflow/run");
    return runApi.request<DetailResult<ArtTherapyWorkflowResponse>>(
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
    const statusApi = new BaseApi(
      `/api/smartDiagnose/art-therapy-workflow/status/${taskId}`
    );
    return statusApi.request<DetailResult<ArtTherapyWorkflowResponse>>(
      "get",
      {},
      {},
      `${statusApi.baseApi}`
    );
  };
}

export const artTherapyWorkflowApi = new ArtTherapyWorkflowApi(
  "/api/smartDiagnose/art-therapy-workflow"
);
export type { ArtTherapyWorkflowRequest, ArtTherapyWorkflowResponse };
