import { BaseApi } from "@/api/base";
import type { BaseResult } from "@/api/types";

class ArtGenerationApi extends BaseApi {
  trigger = (pk: number | string) => {
    return this.request<BaseResult>(
      "post",
      {},
      {},
      `${this.baseApi}/${pk}/trigger_generation`
    );
  };
}

const artGenerationApi = new ArtGenerationApi(
  "/api/smartDiagnose/art-generation-job"
);

export { artGenerationApi };
