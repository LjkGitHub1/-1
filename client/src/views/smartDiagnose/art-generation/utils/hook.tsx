import { artGenerationApi } from "./api";
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

const statusType: Record<
  number,
  { label: string; type: "info" | "warning" | "success" | "danger" }
> = {
  1: { label: "pending", type: "info" },
  2: { label: "running", type: "warning" },
  3: { label: "completed", type: "success" },
  4: { label: "failed", type: "danger" }
};

export function useArtGeneration(tableRef: Ref) {
  const api = reactive(artGenerationApi);
  const auth = reactive({
    trigger_generation: false,
    ...getDefaultAuths(getCurrentInstance(), ["trigger_generation"])
  });
  const { t } = useI18n();

  const operationButtonsProps = shallowRef<OperationProps>({
    width: 320,
    showNumber: 4,
    buttons: [
      {
        text: t("smartDiagnose.artGeneration.trigger"),
        code: "trigger_generation",
        show: auth.trigger_generation,
        props: { type: "primary", link: true },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.trigger(row?.pk ?? row?.id),
            success(res) {
              message(
                t("smartDiagnose.artGeneration.triggerSuccess", {
                  url: res?.data?.output_url ?? "-"
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
      if (column._column?.key === "status") {
        column.cellRenderer = ({ row }) => {
          const meta = statusType[row.status] ?? statusType[1];
          return h(ElTag, { type: meta.type, effect: "dark" }, () =>
            t(`smartDiagnose.artGeneration.status.${meta.label}`)
          );
        };
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
