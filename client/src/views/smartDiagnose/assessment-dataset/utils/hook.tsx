import { assessmentDatasetApi } from "./api";
import { getCurrentInstance, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn
} from "@/components/RePlusPage";

export function useAssessmentDataset(_tableRef: Ref) {
  const api = reactive(assessmentDatasetApi);
  const auth = reactive({
    ...getDefaultAuths(getCurrentInstance(), [])
  });

  const operationButtonsProps = shallowRef<OperationProps>({
    width: 220,
    showNumber: 3
  });

  const listColumnsFormat = (columns: PageTableColumn[]) => columns;
  const searchColumnsFormat = (columns: PageColumn[]) => columns;

  return {
    api,
    auth,
    operationButtonsProps,
    listColumnsFormat,
    searchColumnsFormat
  };
}
