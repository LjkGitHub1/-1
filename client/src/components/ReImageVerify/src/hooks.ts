import { onMounted, ref } from "vue";
import { getCaptchaApi } from "@/api/auth";
import { useUserStoreHook } from "@/store/modules/user";
import { delay } from "@pureadmin/utils";

export const useImageVerify = imgCode => {
  // const imgCode = ref("");
  const imgUrl = ref("");
  const loading = ref(false);

  function getImgCode() {
    loading.value = true;
    getCaptchaApi()
      .then(res => {
        if (res.code === 1000) {
          // 如果返回的是相对路径，确保以 / 开头
          let imageUrl = res.captcha_image;
          if (
            imageUrl &&
            !imageUrl.startsWith("http://") &&
            !imageUrl.startsWith("https://") &&
            !imageUrl.startsWith("/")
          ) {
            imageUrl = "/" + imageUrl;
          }
          // 如果是相对路径，使用当前域名（通过 Nginx 代理）
          if (
            imageUrl &&
            imageUrl.startsWith("/") &&
            !imageUrl.startsWith("http")
          ) {
            imageUrl = window.location.origin + imageUrl;
          }
          imgUrl.value = imageUrl;
          imgCode.value = res.captcha_key;
          useUserStoreHook().SET_VERIFY_CODE_LENGTH(res.length);
        }
      })
      .finally(() => {
        delay(100).then(() => {
          loading.value = false;
        });
      });
  }

  onMounted(() => {
    getImgCode();
  });

  return {
    imgUrl,
    loading,
    imgCode,
    getImgCode
  };
};
