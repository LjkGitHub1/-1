import { emotionFusionApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn
} from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { handleOperation } from "@/components/RePlusPage";
import { message } from "@/utils/message";
import { ElTag } from "element-plus";

export function useEmotionFusion(tableRef: Ref) {
  const api = reactive(emotionFusionApi);
  const auth = reactive({
    analyze: false,
    ...getDefaultAuths(getCurrentInstance(), ["analyze"])
  });
  const { t } = useI18n();

  const operationButtonsProps = shallowRef<OperationProps>({
    width: 280,
    showNumber: 4,
    buttons: [
      {
        text: t("smartDiagnose.emotionFusion.analyze"),
        code: "analyze",
        props: { type: "primary", link: true },
        show: auth.analyze,
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.analyze(row?.pk ?? row?.id, {
              voice: 0.58,
              vision: 0.66,
              bio: 0.61
            }),
            success(res) {
              message(
                t("smartDiagnose.emotionFusion.analyzeSuccess", {
                  emotion: res?.data?.emotion ?? "-",
                  confidence: res?.data?.confidence ?? "-"
                })
              );
              tableRef.value?.handleGetData?.();
            },
            requestEnd() {
              loading.value = false;
            }
          });
        }
      }
    ]
  });

  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "is_active") {
        column.cellRenderer = ({ row }) =>
          h(ElTag, { type: row.is_active ? "success" : "danger" }, () =>
            row.is_active ? t("common.active") : t("common.inactive")
          );
      }
    });
    return columns;
  };
  const searchColumnsFormat = (columns: PageColumn[]) => columns;

  return {
    api,
    auth,
    operationButtonsProps,
    listColumnsFormat,
    searchColumnsFormat
  };
}
