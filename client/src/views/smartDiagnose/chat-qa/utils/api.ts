import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

/**
 * 心理问答接口封装（继承BaseApi，与现有接口风格一致）
 */
class ChatQaApi extends BaseApi {
  /**
   * 发送问题（携带当前用户ID和模型ID）
   */
  sendQuestion = (data: {
    question: string;
    model_id: number | string;
    user_id: number | string;
  }) => {
    const sendQuestionApi = new BaseApi(
      "/api/smartDiagnose/chat-record/send_question"
    );
    return sendQuestionApi.request<BaseResult>(
      "post",
      data,
      {},
      `${sendQuestionApi.baseApi}` // 对应后端action
    );
  };

  /**
   * 获取当前用户对话历史
   */
  getChatHistory = (userId: number | string) => {
    const chatRecordApi = new BaseApi("/api/smartDiagnose/chat-record");
    return chatRecordApi.request<BaseResult>(
      "get",
      {}, // GET 请求通常不传 data，参数放在 params 中
      { user_id: userId }, // 查询参数
      `${chatRecordApi.baseApi}` // 假设对应后端接口路径为 /history
    ); // 复用BaseApi分页查询
  };

  /**
   * 获取已配置的模型列表（对接模型配置模块）
   */
  getModelList = () => {
    const modelApi = new BaseApi("/api/smartDiagnose/model-config");
    return modelApi.request<BaseResult>(
      "get",
      {},
      { status: 1 },
      `${modelApi.baseApi}` // assuming backend exposes a [/list](file://d:\develop\xadmin\beyourself\client\node_modules\yallist) endpoint
    ); // 仅查询启用状态的模型
    console.log("getModelList", modelApi);
  };
}

// 基础路径与后端路由匹配
export const chatQaApi = new ChatQaApi("/api/smartDiagnose/chat-qa");
