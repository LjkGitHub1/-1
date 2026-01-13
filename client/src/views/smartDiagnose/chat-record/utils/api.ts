import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class ChatRecordApi extends BaseApi {
  // 自定义发送问答请求接口
  sendQuestion = (data: any) => {
    return this.request<BaseResult>(
      "post",
      data,
      {},
      `${this.baseApi}/send_question`
    );
  };
}

const chatRecordApi = new ChatRecordApi("/api/smartDiagnose/chat-record");
export { chatRecordApi };
