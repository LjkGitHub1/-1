import { interventionPlanApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn
  // RePlusPageProps
} from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import CircleClose from "~icons/ep/circle-close";
import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { ElTag } from "element-plus";
// import { message } from "@/utils/message";

export function useInterventionPlan(tableRef: Ref) {
  const api = reactive(interventionPlanApi);
  const auth = reactive({
    start: false,
    ...getDefaultAuths(getCurrentInstance(), ["start"])
  });
  const { t } = useI18n();

  // 行操作按钮：启动方案
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 250,
    showNumber: 3,
    buttons: [
      {
        text: t("interventionPlan.startPlan"),
        code: "start",
        confirm: {
          title: row => t("interventionPlan.confirmStart", { no: row.plan_no })
        },
        props: {
          type: "success",
          icon: useRenderIcon(CircleClose),
          link: true
        },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.start(row?.pk ?? row?.id),
            success() {
              tableRef.value.handleGetData();
              // message.success(t("common.operateSuccess"));
            },
            requestEnd() {
              loading.value = false;
            }
          });
        },
        show: auth.start && (row => row.plan_status === 1) // 仅待执行状态显示
      }
    ]
  });

  // 表格列格式化：方案状态标签
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "plan_status") {
        column["cellRenderer"] = ({ row }) => {
          const statusMap = { 1: "info", 2: "success", 3: "default" };
          const statusText = row.get_plan_status_display();
          return h(
            ElTag,
            { type: statusMap[row.plan_status] },
            () => statusText
          );
        };
      }
    });
    return columns;
  };

  // 搜索框格式化：干预类型下拉
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "intervention_type") {
        column.valueType = "select";
        column["fieldProps"]["options"] = [
          { label: "认知行为疗法", value: "认知行为疗法" },
          { label: "正念训练", value: "正念训练" },
          { label: "情绪疏导", value: "情绪疏导" }
        ];
      }
    });
    return columns;
  };

  return {
    api,
    auth,
    operationButtonsProps,
    listColumnsFormat,
    searchColumnsFormat
  };
}
