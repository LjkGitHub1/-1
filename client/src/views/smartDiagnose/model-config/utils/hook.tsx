import { modelConfigApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn
  // RePlusPageProps
} from "@/components/RePlusPage";
// import { useRenderIcon } from "@/components/ReIcon/src/hooks";
// import SwitchButton from "~icons/ep/switch-button";
// import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { ElTag } from "element-plus";
// import { message } from "@/utils/message";

export function useModelConfig(_tableRef: Ref) {
  const api = reactive(modelConfigApi);
  // 按文档规范：权限控制，自动匹配路由权限
  const auth = reactive({
    ...getDefaultAuths(getCurrentInstance(), [])
  });
  const { t } = useI18n();

  // 按文档规范：表格行操作按钮（无额外自定义，默认CRUD）
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 200,
    showNumber: 3
  });

  // 按文档规范：表格列格式化（处理启用状态标签）
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "is_active":
          column["cellRenderer"] = ({ row }) => {
            const tagType = row.is_active ? "success" : "danger";
            const tagText = row.is_active
              ? t("common.active")
              : t("common.inactive");
            return h(ElTag, { type: tagType }, () => tagText);
          };
          break;
      }
    });
    return columns;
  };

  // 按文档规范：搜索框格式化（无特殊处理，默认渲染）
  const searchColumnsFormat = (columns: PageColumn[]) => {
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
