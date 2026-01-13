import { personalizedAssessmentApi } from "./api";
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

const stressType: Record<
  number,
  { label: string; type: "success" | "warning" | "danger" }
> = {
  1: { label: "low", type: "success" },
  2: { label: "medium", type: "warning" },
  3: { label: "high", type: "danger" }
};

const statusType: Record<
  number,
  { label: string; type: "info" | "success" | "warning" }
> = {
  1: { label: "draft", type: "info" },
  2: { label: "generated", type: "success" },
  3: { label: "intervened", type: "warning" }
};

const extractPk = (value: any) => {
  if (value && typeof value === "object") {
    return value.pk ?? value.id;
  }
  return value;
};

export function usePersonalizedAssessment(tableRef: Ref) {
  const api = reactive(personalizedAssessmentApi);
  const auth = reactive({
    refreshPlan: false,
    generateReport: false,
    ...getDefaultAuths(getCurrentInstance(), ["refreshPlan", "generateReport"])
  });
  const { t } = useI18n();

  const operationButtonsProps = shallowRef<OperationProps>({
    width: 360,
    showNumber: 4,
    buttons: [
      {
        text: t("smartDiagnose.personalizedAssessment.refreshPlan"),
        code: "refreshPlan",
        props: {
          type: "primary",
          link: true
        },
        show: auth.refreshPlan,
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.refreshPlan(row?.pk ?? row?.id),
            success() {
              message(t("smartDiagnose.personalizedAssessment.refreshSuccess"));
              tableRef.value?.handleGetData?.();
            },
            requestEnd() {
              loading.value = false;
            }
          });
        }
      },
      {
        text: t("smartDiagnose.personalizedAssessment.cloneGenerate"),
        code: "generateReport",
        props: {
          type: "success",
          link: true
        },
        show: auth.generateReport,
        onClick: ({ row, loading }) => {
          const userPk = extractPk(row.user);
          if (!userPk) {
            message(t("smartDiagnose.personalizedAssessment.missingUser"), {
              type: "warning"
            });
            return;
          }
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.generateReport({
              user: userPk,
              assessment_model: extractPk(row.assessment_model),
              signals: row.signal_snapshot ?? {}
            }),
            success() {
              message(
                t("smartDiagnose.personalizedAssessment.generateSuccess")
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
      if (column._column?.key === "stress_level") {
        column.cellRenderer = ({ row }) => {
          const meta = stressType[row.stress_level] ?? stressType[2];
          return h(ElTag, { type: meta.type, effect: "plain" }, () =>
            t(`smartDiagnose.personalizedAssessment.stress.${meta.label}`)
          );
        };
      }
      if (column._column?.key === "status") {
        column.cellRenderer = ({ row }) => {
          const meta = statusType[row.status] ?? statusType[1];
          return h(ElTag, { type: meta.type }, () =>
            t(`smartDiagnose.personalizedAssessment.status.${meta.label}`)
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
