import { knowledgeBaseApi } from "./api";
import { getCurrentInstance, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type { OperationProps } from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Refresh from "~icons/ep/refresh";
import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { message } from "@/utils/message";

export function useKnowledgeBase(tableRef: Ref) {
  const api = reactive(knowledgeBaseApi);
  const auth = reactive({
    syncDocCount: false,
    ...getDefaultAuths(getCurrentInstance(), ["syncDocCount"])
  });
  const { t } = useI18n();

  // 按文档规范：自定义行操作按钮（同步文档数量）
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 250,
    showNumber: 4,
    buttons: [
      {
        text: t("smartDiagnose.knowledgeBase.syncDocCount"),
        code: "syncDocCount",
        confirm: {
          title: row =>
            t("smartDiagnose.knowledgeBase.confirmSync", { name: row.kb_name })
        },
        props: {
          type: "primary",
          icon: useRenderIcon(Refresh),
          link: true
        },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.syncDocCount(row?.pk ?? row?.id),
            success() {
              tableRef.value.handleGetData(); // 刷新表格
              message(t("common.operateSuccess"));
            },
            requestEnd() {
              loading.value = false;
            }
          });
        },
        show: auth.syncDocCount
      }
    ]
  });

  // 表格列格式化（无特殊处理）
  const listColumnsFormat = (columns: any[]) => columns;
  // 搜索框格式化（无特殊处理）
  const searchColumnsFormat = (columns: any[]) => columns;

  return {
    api,
    auth,
    operationButtonsProps,
    listColumnsFormat,
    searchColumnsFormat
  };
}
