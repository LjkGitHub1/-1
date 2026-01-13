import { eegBdfApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn,
  RePlusPageProps
} from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Check from "~icons/ep/check";
import File from "~icons/ep/files";
import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { message } from "@/utils/message";
import { ElTag } from "element-plus";

export function useEegBdf(tableRef: Ref) {
  const api = reactive(eegBdfApi);
  const auth = reactive({
    add: false,
    edit: false,
    delete: false,
    analyze: false,
    ...getDefaultAuths(getCurrentInstance(), [
      "add",
      "edit",
      "delete",
      "analyze"
    ])
  });
  const { t } = useI18n();

  // 表格列格式化：状态标签、文件路径链接
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "status":
          column.cellRenderer = ({ row }) => {
            const statusMap = { 0: "未处理", 1: "已分析", 2: "异常" };
            const typeMap = { 0: "info", 1: "success", 2: "danger" };
            return h(
              ElTag,
              { type: typeMap[row.status] },
              () => statusMap[row.status]
            );
          };
          break;
        case "bdf_file_path":
          column.cellRenderer = ({ row }) => {
            return h(
              "a",
              {
                href: row.bdf_file_path,
                target: "_blank",
                style:
                  "color: #409eff; text-decoration: underline; font-size: 12px"
              },
              () => t("biofeedback.viewFilePath")
            );
          };
          break;
        case "patient_name":
          column.cellRenderer = ({ row }) => {
            return h(
              ElTag,
              { type: "primary", size: "small" },
              () => row.patient_name || row.name || "-"
            );
          };
          break;
      }
    });
    return columns;
  };

  // 搜索栏格式化：状态下拉、时间范围选择
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "status":
          column.valueType = "select";
          column.fieldProps = {
            options: [
              { label: "未处理", value: 0 },
              { label: "已分析", value: 1 },
              { label: "异常", value: 2 }
            ]
          };
          break;
        case "collect_time":
          // column.valueType = "date-picker";
          // column.fieldProps = { format: "YYYY-MM-DD HH:mm:ss" };
          column.valueType = "date-picker";
          column.fieldProps = {
            format: "YYYY-MM-DD HH:mm:ss",
            type: "datetime",
            valueFormat: "YYYY-MM-DD HH:mm:ss"
          };
          break;
      }
    });
    return columns;
  };

  // 操作按钮：标记分析、编辑、删除
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 300,
    showNumber: 3,
    buttons: [
      {
        text: t("biofeedback.analyze"),
        code: "analyze",
        confirm: { title: t("biofeedback.confirmAnalyze") },
        props: { type: "success", icon: useRenderIcon(Check) },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.analyze(row.pk),
            success() {
              tableRef.value.handleGetData();
              message(t("biofeedback.analyzeSuccess"));
            },
            requestEnd() {
              loading.value = false;
            }
          });
        },
        // 仅未处理状态显示该按钮
        show: auth.analyze && (row => row.status === 0)
      },
      {
        text: t("buttons.edit"),
        code: "edit",
        props: { type: "primary", icon: useRenderIcon(File) },
        show: auth.edit
      },
      {
        text: t("buttons.delete"),
        code: "delete",
        props: { type: "danger" },
        confirm: { title: t("buttons.confirmDelete") },
        show: auth.delete
      }
    ]
  });

  // 新增/编辑配置：关联病人选择、采集时间选择
  const addOrEditOptions = shallowRef<RePlusPageProps["addOrEditOptions"]>({
    props: {
      columns: {
        patient_id: ({ column }) => {
          column.label = t("biofeedback.patient_name");
          column.valueType = "autocomplete";
          column.fieldProps = {
            apiUrl: "/api/biofeedback/patient",
            // some backends return patient name as `name` instead of `patient_name`
            // use the common `name` key for autocomplete; rendering will fallback to patient_name if present
            labelKey: "name",
            valueKey: "pk",
            fetchParams: { page_size: 100 }
          };
          column.required = true;
          return column;
        },
        collect_time: ({ column }) => {
          column.valueType = "date-picker";
          column.fieldProps = {
            type: "datetime",
            format: "YYYY-MM-DD HH:mm:ss",
            placeholder: t("biofeedback.chooseCollectTime")
          };
          column.required = true;
          return column;
        },
        status: ({ column }) => {
          column.valueType = "select";
          column.fieldProps = {
            options: [
              { label: "未处理", value: 0 },
              { label: "已分析", value: 1 },
              { label: "异常", value: 2 }
            ]
          };
          return column;
        },
        bdf_file_path: ({ column }) => {
          column.valueType = "input";
          column.fieldProps = { placeholder: t("biofeedback.enterFilePath") };
          column.required = true;
          return column;
        }
      }
    }
  });

  return {
    api,
    auth,
    listColumnsFormat,
    searchColumnsFormat,
    operationButtonsProps,
    addOrEditOptions
  };
}
