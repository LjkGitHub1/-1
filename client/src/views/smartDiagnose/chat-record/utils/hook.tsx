import { chatRecordApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type { OperationProps } from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Promotion from "~icons/ep/promotion";
import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { message } from "@/utils/message";
import { ElTag } from "element-plus";

export function useChatRecord(_tableRef: Ref) {
  const api = reactive(chatRecordApi);
  const auth = reactive({
    sendQuestion: false,
    ...getDefaultAuths(getCurrentInstance(), ["sendQuestion"])
  });
  const { t } = useI18n();

  // 按文档规范：表格标题栏按钮（发送问答请求）
  const tableBarButtonsProps = shallowRef<OperationProps>({
    buttons: [
      {
        text: t("smartDiagnose.chatRecord.sendQuestion"),
        code: "sendQuestion",
        props: {
          type: "success",
          icon: useRenderIcon(Promotion),
          plain: true
        },
        onClick: () => {
          // 模拟选择用户后发送请求（实际需弹窗选择用户）
          const testData = {
            user_id: 1,
            question: t("smartDiagnose.chatRecord.testQuestion")
          };
          handleOperation({
            t,
            apiReq: api.sendQuestion(testData),
            success(res) {
              message(t("common.operateSuccess"));
              console.log("问答结果：", res.data);
            }
          });
        },
        show: auth.sendQuestion
      }
    ]
  });

  // 表格列格式化（情绪结果标签）
  const listColumnsFormat = (columns: any[]) => {
    columns.forEach(column => {
      if (column._column?.key === "emotion_result") {
        column["cellRenderer"] = ({ row }) => {
          return h(ElTag, { type: "warning" }, () => row.emotion_result);
        };
      }
    });
    return columns;
  };

  const searchColumnsFormat = (columns: any[]) => columns;
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 200,
    showNumber: 3
  });

  return {
    api,
    auth,
    operationButtonsProps,
    listColumnsFormat,
    searchColumnsFormat,
    tableBarButtonsProps
  };
}
