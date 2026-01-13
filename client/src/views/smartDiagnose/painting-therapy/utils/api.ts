import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class PaintingTherapyApi extends BaseApi {
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

const paintingTherapyApi = new PaintingTherapyApi(
  "/api/smartDiagnose/painting-therapy"
);
export { paintingTherapyApi };
