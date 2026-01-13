import { reactive, ref } from "vue";
import { chatQaApi } from "./api";
import { useI18n } from "vue-i18n";
import { ElMessage } from "element-plus";
import { userInfoApi } from "@/api/user/userinfo";
import { chatRecordApi } from "../../chat-record/utils/api";
// import type { BaseResult } from "@/api/types";

export function useChatQa() {
  const { t } = useI18n();
  // const userStore = useUserStoreHook(); // 当前登录用户信息

  // 状态管理（与现有代码reactive风格一致）
  const state = reactive({
    // 模型相关
    modelList: [] as Array<{ id: number; name: string; desc: string }>,
    selectedModelId: null as number | null,
    modelLoading: false,

    // 对话相关
    chatList: [] as Array<{
      id: string;
      role: "user" | "ai";
      content: string;
      timestamp: string;
      modelName: string;
    }>,
    inputContent: "",
    sending: false,
    historyLoading: false
  });

  const userId = ref(null);
  // 调用接口获取用户信息，其中包含 pk
  // 在 hook.tsx 中修改 userInfoApi 的调用逻辑
  const initUserId = async () => {
    try {
      const res = await userInfoApi.retrieve();
      if (res.code === 1000) {
        userId.value = res.data.pk;
        console.log("用户 ID:", userId.value);
        // 获取到 userId 后再执行初始化
        init();
      }
    } catch (err) {
      console.error("获取用户信息失败", err);
      ElMessage.error(t("common.getUserIdFail")); // 假设添加了对应翻译
    }
  };

  // 页面加载时先获取用户信息，再初始化
  initUserId();

  /**
   * 初始化：加载模型列表+当前用户历史对话
   */

  const init = async () => {
    // 校验登录状态（与现有权限逻辑一致）
    console.log("init中打印用户 ID:", userId.value);
    if (!userId.value) {
      ElMessage.error(t("common.notLogin"));
      return;
    }

    // 并行加载模型和历史（提升性能）
    state.modelLoading = true;
    state.historyLoading = true;
    try {
      const modelRes: any = await chatQaApi.getModelList();
      const historyRes: any = await chatQaApi.getChatHistory(userId.value);

      // 处理模型列表
      // const modelData = Array.isArray(modelRes.data.Res) ? modelRes.data : [];
      console.log("modelData", modelRes.data.results);
      state.modelList = modelRes.data.results.map(item => ({
        id: item.pk,
        name: item.model_name,
        desc: item.description || t("common.noDesc")
      }));
      if (state.modelList.length > 0) {
        state.selectedModelId = state.modelList[0].id; // 默认选中第一个
      }

      // 处理历史对话
      const historyData = historyRes.data.results || [];
      console.log("historyData", historyData);
      state.chatList = formatChatHistory(historyData);
    } catch (err) {
      console.error("Initialization failed", err); // Optional: log the error for debugging
      ElMessage.error(t("chatQa.initFail"));
    } finally {
      state.modelLoading = false;
      state.historyLoading = false;
    }
  };

  /**
   * 格式化历史对话数据
   */
  const formatChatHistory = (history: any[]) => {
    return history.flatMap(item => [
      {
        id: `user-${item.id}`,
        role: "user" as const,
        content: item.question,
        timestamp: formatTime(item.create_time),
        modelName: item.model_name
      },
      {
        id: `ai-${item.id}`,
        role: "ai" as const,
        content: item.answer || t("chatQa.noAnswer"),
        timestamp: formatTime(item.answer_time || item.create_time),
        modelName: item.model_name
      }
    ]);
  };

  /**
   * 时间格式化工具
   */
  const formatTime = (timeStr: string) => {
    const date = new Date(timeStr);
    return date.toLocaleString();
  };

  /**
   * 发送问题
   */
  const sendQuestion = async () => {
    // 输入校验（与现有表单校验逻辑一致）
    if (!state.selectedModelId) {
      ElMessage.warning(t("chatQa.chooseModelFirst"));
      return;
    }
    if (!state.inputContent.trim()) {
      ElMessage.warning(t("chatQa.inputQuestionFirst"));
      return;
    }
    if (!userId.value) {
      ElMessage.error(t("common.notLogin"));
      return;
    }

    // 临时添加用户消息（优化体验）
    const tempId = `temp-${Date.now()}`;
    const model = state.modelList.find(m => m.id === state.selectedModelId);
    state.chatList.push({
      id: tempId,
      role: "user",
      content: state.inputContent,
      timestamp: formatTime(new Date().toString()),
      modelName: model?.name || ""
    });
    state.sending = true;
    const originalContent = state.inputContent;
    state.inputContent = "";

    try {
      // 调用接口发送问题
      const res: any = await chatRecordApi.sendQuestion({
        question: originalContent,
        model_id: state.selectedModelId,
        user_id: userId.value
        // created_time: new Date().toISOString(),
        // updated_time: new Date().toISOString()
      });

      // 替换临时消息+添加AI回复
      state.chatList = state.chatList.filter(item => item.id !== tempId);
      state.chatList.push(
        {
          id: `user-${res.data.id}`,
          role: "user",
          content: originalContent,
          timestamp: formatTime(new Date().toString()),
          modelName: model?.name || ""
        },
        {
          id: `ai-${res.data.id}`,
          role: "ai",
          content: res.data.answer,
          timestamp: formatTime(new Date().toString()),
          modelName: model?.name || ""
        }
      );
    } catch (err) {
      // 失败回滚临时消息
      state.chatList = state.chatList.filter(item => item.id !== tempId);
      state.inputContent = originalContent;
      console.error("Send question failed", err); // Optional: log the error for debugging
      ElMessage.error(t("chatQa.sendFail"));
    } finally {
      state.sending = false;
    }
  };

  return {
    state,
    init,
    sendQuestion,
    formatTime
  };
}
