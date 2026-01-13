import { emotionRecognitionApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type { PageTableColumn, OperationProps } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { ElTag } from "element-plus";

export function useEmotionRecognition(_tableRef: Ref) {
  const api = reactive(emotionRecognitionApi);
  const auth = reactive({
    ...getDefaultAuths(getCurrentInstance(), [])
  });
  const { t } = useI18n();

  // 按文档规范：表格列格式化（识别类型标签）
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "supported_type") {
        column["cellRenderer"] = ({ row }) => {
          const typeMap = { 1: "text", 2: "voice", 3: "image" };
          const typeText = t(
            `smartDiagnose.emotionRecognition.type.${typeMap[row.supported_type]}`
          );
          return h(ElTag, { type: "info" }, () => typeText);
        };
      }
    });
    return columns;
  };

  const searchColumnsFormat = (columns: any[]) => columns;
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
