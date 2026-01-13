import { patientApi } from "./api";
import { getCurrentInstance, h, reactive, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn,
  RePlusPageProps
} from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import User from "~icons/ep/user";
import Delete from "~icons/ep/delete";
import { useI18n } from "vue-i18n";
import { ElTag } from "element-plus";

export function usePatient() {
  const api = reactive(patientApi);
  const auth = reactive({
    add: false,
    edit: false,
    delete: false,
    ...getDefaultAuths(getCurrentInstance(), ["add", "edit", "delete"])
  });
  const { t } = useI18n();

  // 表格列格式化：性别、科室标签展示
  const listColumnsFormat = (columns: PageTableColumn[]) => {
    columns.forEach(column => {
      switch (column._column?.key) {
        case "gender":
          column.cellRenderer = ({ row }) => {
            const genderMap = { 0: "未知", 1: "男", 2: "女" };
            const typeMap = { 0: "info", 1: "primary", 2: "success" };
            return h(
              ElTag,
              { type: typeMap[row.gender.value] },
              () => genderMap[row.gender.value]
            );
          };
          break;
        case "department":
          column.cellRenderer = ({ row }) => {
            return row.department
              ? h(
                  ElTag,
                  { type: "warning", size: "small" },
                  () => row.department
                )
              : h(ElTag, { type: "info", size: "small" }, () => "未填写");
          };
          break;
      }
    });
    return columns;
  };

  // 搜索栏格式化：性别下拉选择
  const searchColumnsFormat = (columns: PageColumn[]) => {
    columns.forEach(column => {
      if (column._column?.key === "gender") {
        column.valueType = "select";
        column.fieldProps = {
          options: [
            { label: t("biofeedback.genderUnknown"), value: 0 },
            { label: t("biofeedback.genderMale"), value: 1 },
            { label: t("biofeedback.genderFemale"), value: 2 }
          ]
        };
      }
    });
    return columns;
  };

  // 操作按钮配置
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 250,
    showNumber: 3,
    buttons: [
      {
        text: t("buttons.edit"),
        code: "edit",
        props: { type: "primary", icon: useRenderIcon(User) },
        show: auth.edit
      },
      {
        text: t("buttons.delete"),
        code: "delete",
        props: { type: "danger", icon: useRenderIcon(Delete) },
        confirm: { title: t("buttons.confirmDelete") },
        show: auth.delete
      }
    ]
  });

  // 新增/编辑配置：出生日期日期选择器
  const addOrEditOptions = shallowRef<RePlusPageProps["addOrEditOptions"]>({
    props: {
      columns: {
        birth_date: ({ column }) => {
          column.valueType = "date-picker";
          column.fieldProps = {
            type: "date",
            format: "YYYY-MM-DD",
            valueFormat: "YYYY-MM-DD", // This ensures the value format
            placeholder: t("biofeedback.chooseBirthDate")
          };
          return column;
        },
        first_visit_time: ({ column }) => {
          column.valueType = "date-picker";
          column.fieldProps = {
            type: "datetime",
            format: "YYYY-MM-DD HH:mm:ss",
            placeholder: t("biofeedback.chooseVisitTime")
          };
          return column;
        },
        gender: ({ column }) => {
          column.valueType = "select";
          column.fieldProps = {
            options: [
              { label: t("biofeedback.genderUnknown"), value: 0 },
              { label: t("biofeedback.genderMale"), value: 1 },
              { label: t("biofeedback.genderFemale"), value: 2 }
            ]
          };
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
