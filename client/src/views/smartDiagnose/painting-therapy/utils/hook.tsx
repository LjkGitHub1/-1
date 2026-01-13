import { paintingTherapyApi } from "./api";
import { getCurrentInstance, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type { PageColumn, OperationProps } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";

export function usePaintingTherapy(_tableRef: Ref) {
  const api = reactive(paintingTherapyApi);
  const auth = reactive({
    ...getDefaultAuths(getCurrentInstance(), [])
  });
  const { t } = useI18n();

  // 按文档规范：自定义搜索框（风格选项JSON编辑器）
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "style_options") {
        column.valueType = "json-editor" as any;
        column["fieldProps"]["height"] = 200;
        column["fieldProps"]["placeholder"] = t(
          "smartDiagnose.paintingTherapy.styleHint"
        );
      }
    });
    return columns;
  };

  const listColumnsFormat = (columns: any[]) => columns;
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 200,
    showNumber: 3
  });

  return {
    api,
    auth,
    operationButtonsProps,
    listColumnsFormat,
    searchColumnsFormat
  };
}
