import { pdfReportApi } from "./api";
import { getCurrentInstance, h, reactive, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn,
  RePlusPageProps
} from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Download from "~icons/ep/download";
import FileText from "~icons/ep/files";
import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { message } from "@/utils/message";
import { ElTag, ElLink } from "element-plus";

export function usePdfReport() {
  const api = reactive(pdfReportApi);
  const auth = reactive({
    add: false,
    edit: false,
    delete: false,
    download: false,
    ...getDefaultAuths(getCurrentInstance(), [
      "add",
      "edit",
      "delete",
      "download"
    ])
  });
  const { t } = useI18n();

  // 表格列格式化：报告类型标签、下载链接
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "report_type":
          column.cellRenderer = ({ row }) => {
            const typeMap = {
              常规脑电分析报告: "primary",
              睡眠分期报告: "success",
              癫痫波检测报告: "warning"
            };
            return h(
              ElTag,
              { type: typeMap[row.report_type] || "info" },
              () => row.report_type
            );
          };
          break;
        case "report_file_path":
          column.cellRenderer = ({ row }) => {
            return h(
              ElLink,
              {
                type: "primary",
                size: "small",
                onClick: () => handleDownload(row.pk)
              },
              () => t("biofeedback.downloadReport")
            );
          };
          break;
        case "report_version":
          column.cellRenderer = ({ row }) => {
            return h(
              ElTag,
              { type: "info", border: true },
              () => row.report_version
            );
          };
          break;
      }
    });
    return columns;
  };

  // 下载报告处理函数
  const handleDownload = (pk: number | string) => {
    handleOperation({
      t,
      apiReq: api.download(pk),
      success: (res: any) => {
        // 生成下载链接并触发下载
        const link = document.createElement("a");
        link.href = res.data.download_url;
        link.download = res.data.download_url.split("/").pop() || "report.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        message(t("biofeedback.downloadStart"));
      }
    });
  };

  // 搜索栏格式化：报告类型下拉、时间范围
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "report_type":
          column.valueType = "select";
          column.fieldProps = {
            options: [
              { label: "常规脑电分析报告", value: "常规脑电分析报告" },
              { label: "睡眠分期报告", value: "睡眠分期报告" },
              { label: "癫痫波检测报告", value: "癫痫波检测报告" }
            ]
          };
          break;
        case "generate_time":
          column.valueType = "date-picker";
          column.fieldProps = { format: "YYYY-MM-DD HH:mm:ss" };
          break;
      }
    });
    return columns;
  };

  // 操作按钮：下载、编辑、删除
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 300,
    showNumber: 3,
    buttons: [
      {
        text: t("biofeedback.downloadReport"),
        code: "download",
        props: { type: "info", icon: useRenderIcon(Download) },
        confirm: { title: t("biofeedback.confirmDownload") },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleDownload(row.pk);
          loading.value = false;
        },
        show: auth.download
      },
      {
        text: t("buttons.edit"),
        code: "edit",
        props: { type: "primary", icon: useRenderIcon(FileText) },
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

  // 新增/编辑配置：关联病人、BDF数据选择
  const addOrEditOptions = shallowRef<RePlusPageProps["addOrEditOptions"]>({
    props: {
      columns: {
        patient_id: ({ column }) => {
          column.label = t("biofeedback.patient_name");
          column.valueType = "autocomplete";
          column.fieldProps = {
            apiUrl: "/api/biofeedback/patient",
            labelKey: "name",
            valueKey: "pk",
            fetchParams: { page_size: 100 }
          };
          column.required = true;
          return column;
        },
        bdf_id: ({ column }) => {
          column.label = t("biofeedback.bdf_file_name");
          column.valueType = "autocomplete";
          column.fieldProps = {
            apiUrl: "/api/biofeedback/eeg-bdf",
            labelKey: "bdf_file_name",
            valueKey: "pk",
            fetchParams: { page_size: 100 }
          };
          column.required = false;
          return column;
        },
        generate_time: ({ column }) => {
          column.valueType = "date-picker";
          column.fieldProps = {
            format: "YYYY-MM-DD HH:mm:ss",
            placeholder: t("biofeedback.chooseGenerateTime")
          };
          column.required = true;
          return column;
        },
        report_type: ({ column }) => {
          column.valueType = "select";
          column.fieldProps = {
            options: [
              { label: "常规脑电分析报告", value: "常规脑电分析报告" },
              { label: "睡眠分期报告", value: "睡眠分期报告" },
              { label: "癫痫波检测报告", value: "癫痫波检测报告" }
            ]
          };
          column.required = true;
          return column;
        },
        report_version: ({ column }) => {
          column.valueType = "input";
          column.fieldProps = { placeholder: t("biofeedback.enterVersion") };
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
