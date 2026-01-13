import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class EmotionFusionApi extends BaseApi {
  analyze = (pk: number | string, payload: Record<string, any>) => {
    return this.request<BaseResult>(
      "post",
      payload,
      {},
      `${this.baseApi}/${pk}/analyze`
    );
  };
}

const emotionFusionApi = new EmotionFusionApi(
  "/api/smartDiagnose/emotion-fusion"
);

export { emotionFusionApi };
