import { assessmentModelApi } from "./api";
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

const statusTypeMap: Record<
  number,
  { textKey: string; type: "warning" | "info" | "success" | "danger" }
> = {
  1: { textKey: "pending", type: "info" },
  2: { textKey: "running", type: "warning" },
  3: { textKey: "success", type: "success" },
  4: { textKey: "failed", type: "danger" }
};

export function useAssessmentModel(tableRef: Ref) {
  const api = reactive(assessmentModelApi);
  const auth = reactive({
    train: false,
    ...getDefaultAuths(getCurrentInstance(), ["train"])
  });
  const { t } = useI18n();

  const operationButtonsProps = shallowRef<OperationProps>({
    width: 300,
    showNumber: 4,
    buttons: [
      {
        text: t("smartDiagnose.assessmentModel.train"),
        code: "train",
        props: {
          type: "primary",
          link: true
        },
        show: auth.train,
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.train(row?.pk ?? row?.id),
            success() {
              message(t("smartDiagnose.assessmentModel.trainSuccess"));
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
      if (column._column?.key === "training_status") {
        column.cellRenderer = ({ row }) => {
          const meta = statusTypeMap[row.training_status] ?? statusTypeMap[1];
          return h(ElTag, { type: meta.type, effect: "light" }, () =>
            t(`smartDiagnose.assessmentModel.status.${meta.textKey}`)
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
