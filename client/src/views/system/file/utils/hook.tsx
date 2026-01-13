import { useI18n } from "vue-i18n";
import { systemUploadFileApi } from "@/api/system/file";
import { getDefaultAuths, hasAuth } from "@/router/utils";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import {
  isUrl,
  openDialogDrawer,
  type OperationProps,
  type PageTableColumn,
  type RePlusPageProps
} from "@/components/RePlusPage";
import uploadForm from "../components/upload.vue";
import { ElIcon, ElLink, ElText } from "element-plus";
import { Link } from "@element-plus/icons-vue";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Upload from "~icons/ep/upload";
import { formatBytes } from "@pureadmin/utils";

export function useSystemUploadFile(tableRef: Ref) {
  const { t } = useI18n();

  const api = reactive(systemUploadFileApi);

  const auth = reactive({
    ...getDefaultAuths(getCurrentInstance()),
    upload: hasAuth("upload:SystemUploadFile"),
    config: hasAuth("config:SystemUploadFile")
  });

  const operationButtonsProps = shallowRef<OperationProps>({});
  const tableBarButtonsProps = shallowRef<OperationProps>({
    buttons: [
      {
        code: "upload",
        text: t("systemUploadFile.upload"),
        props: {
          type: "success",
          icon: useRenderIcon(Upload)
        },
        onClick: () => {
          openDialogDrawer({
            t,
            title: t("systemUploadFile.upload"),
            rawRow: {},
            rawColumns: [],
            dialogDrawerOptions: { width: "600px", hideFooter: true },
            minWidth: "600px",
            form: uploadForm,
            props: {
              tableRef: () => {
                return tableRef;
              }
            }
          });
        },
        show: auth.upload && auth.config && 3
      }
    ]
  });

  const addOrEditOptions = shallowRef<RePlusPageProps["addOrEditOptions"]>({
    props: {
      formProps: {
        rules: ({ rawFormProps: { rules }, isAdd, rawRow }) => {
          if (isAdd || !rawRow?.is_upload) {
            const fileUrlRule = rules["file_url"][0];
            rules["file_url"] = [
              {
                required: true,
                validator: (rule, value, callback) => {
                  if (!isUrl(value)) {
                    callback(new Error(fileUrlRule?.message));
                  } else {
                    callback();
                  }
                },
                trigger: "blur"
              }
            ];
          }
          return rules;
        }
      }
    }
  });

  const listColumnsFormat = (columns: PageTableColumn[]) => {
    let userColumnIndex = -1;

    // 需要隐藏的列
    const hiddenColumns = ["pk", "is_tmp", "is_upload", "md5sum"];

    // 过滤掉需要隐藏的列
    const filteredColumns = columns.filter(
      column => !hiddenColumns.includes(column._column?.key)
    );

    filteredColumns.forEach((column, index) => {
      switch (column._column?.key) {
        case "access_url":
          column["cellRenderer"] = ({ row }) =>
            h(
              ElLink,
              {
                type: "success",
                href: row[column._column?.key],
                target: "_blank"
              },
              {
                icon: () => h(ElIcon, null, () => h(Link)),
                default: () => t("systemUploadFile.fileLink")
              }
            );
          break;
        case "filesize":
          column["cellRenderer"] = ({ row }) =>
            h(ElText, { type: "primary" }, () => {
              return formatBytes(row[column._column?.key]);
            });
          break;
        case "user":
          userColumnIndex = index;
          column["cellRenderer"] = ({ row }) => {
            const user = row.user;
            if (!user) return h(ElText, { type: "info" }, () => "-");
            const displayName = user.nickname || user.username;
            return h(ElText, { type: "primary" }, () => displayName);
          };
          break;
        case "created_time":
          column["cellRenderer"] = ({ row }) => {
            if (!row.created_time)
              return h(ElText, { type: "info" }, () => "-");
            const date = new Date(row.created_time);
            return h(ElText, { type: "info" }, () =>
              date.toLocaleString("zh-CN", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
              })
            );
          };
          break;
        case "description":
          column["cellRenderer"] = ({ row }) => {
            if (!row.description) return h(ElText, { type: "info" }, () => "-");
            return h(ElText, { type: "info" }, () => row.description);
          };
          break;
      }
    });

    // 在用户列后面添加病历号列
    if (userColumnIndex >= 0) {
      // 先检查是否已经存在病历号列，如果存在则移除
      const existingIndex = filteredColumns.findIndex(
        col => col._column?.key === "medical_record_no"
      );
      if (existingIndex >= 0) {
        filteredColumns.splice(existingIndex, 1);
        // 如果移除的列在用户列之前，需要调整 userColumnIndex
        if (existingIndex <= userColumnIndex) {
          userColumnIndex--;
        }
      }

      // 在用户列后面插入病历号列
      filteredColumns.splice(userColumnIndex + 1, 0, {
        _column: { key: "medical_record_no", label: "病历号" },
        label: "病历号",
        prop: "medical_record_no",
        width: 150,
        cellRenderer: ({ row }) => {
          const user = row.user;
          if (!user || !user.medical_record_no) {
            return h(ElText, { type: "info" }, () => "-");
          }
          return h(ElText, { type: "primary" }, () => user.medical_record_no);
        }
      } as PageTableColumn);
    }

    return filteredColumns;
  };
  return {
    api,
    auth,
    listColumnsFormat,
    addOrEditOptions,
    tableBarButtonsProps,
    operationButtonsProps
  };
}
