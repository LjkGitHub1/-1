import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class EmotionRecognitionApi extends BaseApi {
  // 无自定义接口
  push = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/push`
    );
  };
}

const emotionRecognitionApi = new EmotionRecognitionApi(
  "/api/smartDiagnose/emotion-recognition"
);
export { emotionRecognitionApi };
