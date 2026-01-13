import { assessmentReportApi } from "./api";
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
import { message } from "@/utils/message";

export function useAssessmentReport(tableRef: Ref) {
  const api = reactive(assessmentReportApi);
  // 权限控制（自动匹配路由权限）
  const auth = reactive({
    archive: false,
    ...getDefaultAuths(getCurrentInstance(), ["archive"])
  });
  const { t } = useI18n();

  // 表格行操作按钮：归档
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 250,
    showNumber: 3,
    buttons: [
      {
        text: t("assessmentReport.archiveReport"),
        code: "archive",
        confirm: {
          title: row =>
            t("assessmentReport.confirmArchive", { no: row.report_no })
        },
        props: {
          type: "primary",
          icon: useRenderIcon(CircleClose),
          link: true
        },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.archive(row?.pk ?? row?.id),
            success() {
              tableRef.value.handleGetData(); // 刷新表格
              message(t("common.operateSuccess"));
            },
            requestEnd() {
              loading.value = false;
            }
          });
        },
        show: auth.archive // 按权限显示
      }
    ]
  });

  // 表格列格式化：风险等级标签
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "risk_level":
          column["cellRenderer"] = ({ row }) => {
            let tagType: "success" | "warning" | "danger" = "success";
            if (row.risk_level === 2) tagType = "warning";
            if (row.risk_level === 3) tagType = "danger";
            return h(ElTag, { type: tagType }, () => row.risk_level_text);
          };
          break;
        case "report_status":
          column["cellRenderer"] = ({ row }) => {
            const statusMap = { 1: "draft", 2: "success", 3: "info" };
            return h(ElTag, { type: statusMap[row.report_status] }, () =>
              row.get_report_status_display()
            );
          };
          break;
      }
    });
    return columns;
  };

  // 搜索框格式化：评估类型下拉
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "assess_type") {
        column.valueType = "select";
        column["fieldProps"]["options"] = [
          { label: "情绪测评", value: "情绪测评" },
          { label: "人格测评", value: "人格测评" },
          { label: "压力测评", value: "压力测评" }
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
