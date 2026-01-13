import { knowledgeDocApi } from "./api";
import { getCurrentInstance, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type { PageColumn, OperationProps } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";

export function useKnowledgeDoc(_tableRef: Ref) {
  const api = reactive(knowledgeDocApi);
  const auth = reactive({
    ...getDefaultAuths(getCurrentInstance(), [])
  });
  const { t } = useI18n();

  // 按文档规范：自定义搜索框（知识库下拉选择）
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "kb") {
        // 匹配后端serializer的input_type
        column.valueType = "api-search-knowledgebase" as any;
        column["fieldProps"]["placeholder"] = t(
          "smartDiagnose.knowledgeDoc.selectKb"
        );
      }
    });
    return columns;
  };

  // 表格列格式化（无特殊处理）
  const listColumnsFormat = (columns: any[]) => columns;
  // 行操作按钮（默认）
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
