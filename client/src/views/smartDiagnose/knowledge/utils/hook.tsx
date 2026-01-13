import { knowledgeApi } from "./api";
import { getCurrentInstance, h, reactive, type Ref, shallowRef } from "vue";
import { getDefaultAuths } from "@/router/utils";
import type {
  OperationProps,
  PageColumn,
  PageTableColumn
} from "@/components/RePlusPage";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Delete from "~icons/ep/delete";
import Search from "~icons/ep/search";
import Add from "~icons/ep/plus";
import { handleOperation } from "@/components/RePlusPage";
import { useI18n } from "vue-i18n";
import { message } from "@/utils/message";
import { ElTag } from "element-plus";
import type { CreateDatasetParams, RetrieveParams } from "./api";

export function useKnowledge(tableRef: Ref) {
  // 权限判断
  const api = reactive(knowledgeApi);
  const auth = reactive({
    list: false,
    create: false,
    delete: false,
    retrieve: false,
    ...getDefaultAuths(getCurrentInstance(), [
      "list",
      "create",
      "delete",
      "retrieve"
    ])
  });
  const { t } = useI18n();

  /**
   * 核心修改：固定表格字段配置（无需后端返回，直接定义）
   * 包含列表字段、搜索字段，与国际化配置对应
   */
  const fixedColumns = shallowRef<{
    listColumns: PageTableColumn[]; // 表格列表字段
    searchColumns: PageColumn[]; // 搜索栏字段
  }>({
    listColumns: [
      {
        _column: {}, // 添加此行以满足 PageTableColumn 接口要求
        label: t("knowledge.name"),
        prop: "name",
        width: 200,
        // ellipsis: true // 文本超出省略
        cellRenderer: ({ row }) =>
          h(
            "span",
            { style: { overflow: "hidden", textOverflow: "ellipsis" } },
            row.name
          ) // ✅ Custom ellipsis
      },
      {
        _column: {}, // 添加此行以满足 PageTableColumn 接口要求
        label: t("knowledge.description"),
        prop: "description",
        width: 300,
        cellRenderer: ({ row }) =>
          h(
            "span",
            { style: { overflow: "hidden", textOverflow: "ellipsis" } },
            row.description
          )
      },
      {
        _column: {},
        label: t("knowledge.provider"),
        prop: "provider",
        width: 120
      },
      {
        _column: {},
        label: t("knowledge.permission"),
        prop: "permission",
        width: 150
      },
      {
        _column: {},
        label: t("knowledge.indexing_technique"),
        prop: "indexing_technique",
        width: 150
      },
      {
        _column: {},
        label: t("knowledge.document_count"),
        prop: "document_count",
        width: 120,
        align: "center"
      },
      {
        _column: {},
        label: t("knowledge.word_count"),
        prop: "word_count",
        width: 120,
        align: "center"
      },
      {
        _column: {},
        label: t("knowledge.created_at"),
        prop: "created_at",
        width: 180,
        align: "center",
        // 时间格式化（毫秒转日期）
        cellRenderer: ({ row }) => new Date(row.created_at).toLocaleString()
      },
      {
        _column: {},
        label: t("knowledge.operation"),
        prop: "operation",
        width: 250,
        align: "center"
      }
    ],
    searchColumns: [
      {
        _column: {},
        prop: "name",
        title: t("knowledge.name"),
        dataIndex: "name",
        key: "name",
        valueType: "input",
        placeholder: t("knowledge.searchByName")
      },
      {
        _column: {},
        prop: "provider",
        title: t("knowledge.provider"),
        dataIndex: "provider",
        key: "provider",
        valueType: "select", // 下拉选择搜索
        fieldProps: {
          options: [
            { label: t("knowledge.providerVendor"), value: "vendor" },
            { label: t("knowledge.providerExternal"), value: "external" }
          ]
        }
      },
      {
        _column: {},
        prop: "permission",
        title: t("knowledge.permission"),
        dataIndex: "permission",
        key: "permission",
        valueType: "select",
        fieldProps: {
          options: [
            { label: t("knowledge.permissionOnlyMe"), value: "only_me" },
            {
              label: t("knowledge.permissionAllTeam"),
              value: "all_team_members"
            },
            {
              label: t("knowledge.permissionPartial"),
              value: "partial_members"
            }
          ]
        }
      }
    ]
  });

  /**
   * 表格行操作按钮（查看、删除、检索测试）
   */
  const operationButtonsProps = shallowRef<OperationProps>({
    width: 300,
    showNumber: 3,
    buttons: [
      // 查看详情
      {
        text: t("knowledge.viewDetail"),
        code: "view",
        props: {
          type: "primary",
          link: true
        },
        onClick: ({ row }) => {
          message(`查看知识库：${row.name}`);
        },
        show: auth.list
      },
      // 检索测试
      {
        text: t("knowledge.retrieveTest"),
        code: "retrieve",
        props: {
          type: "success",
          icon: useRenderIcon(Search)
        },
        onClick: async ({ row, loading }) => {
          loading.value = true;
          const retrieveParams: RetrieveParams = {
            query: "测试检索",
            retrieval_model: {
              search_method: "hybrid_search",
              reranking_enable: true,
              top_k: 10,
              score_threshold_enabled: false
            }
          };
          handleOperation({
            t,
            apiReq: api.retrieve(row.id, retrieveParams),
            success: res => {
              message(t("knowledge.retrieveSuccess"));
              console.log("检索结果：", res.data.records);
            },
            requestEnd: () => {
              loading.value = false;
            }
          });
        },
        show: auth.retrieve
      },
      // 删除知识库
      {
        text: t("knowledge.delete"),
        code: "delete",
        confirm: {
          title: row => t("knowledge.confirmDelete", { name: row.name })
        },
        props: {
          type: "danger",
          icon: useRenderIcon(Delete)
        },
        onClick: ({ row, loading }) => {
          loading.value = true;
          handleOperation({
            t,
            apiReq: api.deleteDataset(row.id),
            success: () => {
              message(t("knowledge.deleteSuccess"));
              tableRef.value.handleGetData(); // 刷新表格
            },
            requestEnd: () => {
              loading.value = false;
            }
          });
        },
        show: auth.delete
      }
    ]
  });

  /**
   * 表格标题栏按钮（新增知识库）
   */
  const tableBarButtonsProps = shallowRef<OperationProps>({
    buttons: [
      {
        text: t("knowledge.create"),
        code: "create",
        props: {
          type: "success",
          icon: useRenderIcon(Add)
        },
        onClick: () => {
          const createParams: CreateDatasetParams = {
            name: "新知识库",
            description: "通过前端固定字段创建的知识库",
            indexing_technique: "high_quality",
            permission: "only_me",
            provider: "vendor",
            embedding_model: "text-embedding-3-small",
            embedding_model_provider: "openai"
          };
          handleOperation({
            t,
            apiReq: api.create(createParams),
            success: () => {
              message(t("knowledge.createSuccess"));
              tableRef.value.handleGetData(); // 刷新表格
            }
          });
        },
        show: auth.create
      }
    ]
  });

  /**
   * 表格列格式化（标签展示）
   * 基于固定字段的key匹配，无需依赖后端返回列结构
   */
  const listColumnsFormat = (_columns: PageTableColumn[]) => {
    // 直接使用固定字段，覆盖原有列配置
    const newColumns = [...fixedColumns.value.listColumns];
    newColumns.forEach(column => {
      switch (column.prop) {
        // 提供商标签展示
        case "provider":
          column.cellRenderer = ({ row }) => {
            const label =
              row.provider === "vendor"
                ? t("knowledge.providerVendor")
                : t("knowledge.providerExternal");
            const type = row.provider === "vendor" ? "primary" : "info";
            return h(ElTag, { type }, () => label);
          };
          break;
        // 权限标签展示
        case "permission":
          column.cellRenderer = ({ row }) => {
            let label = "";
            let type = "default";
            switch (row.permission) {
              case "only_me":
                label = t("knowledge.permissionOnlyMe");
                type = "warning";
                break;
              case "all_team_members":
                label = t("knowledge.permissionAllTeam");
                type = "success";
                break;
              case "partial_members":
                label = t("knowledge.permissionPartial");
                type = "info";
                break;
            }
            return h(ElTag, { type: type as any }, () => label);
          };
          break;
        // 索引技术格式化
        case "indexing_technique":
          column.cellRenderer = ({ row }) => {
            return row.indexing_technique === "high_quality"
              ? t("knowledge.indexHighQuality")
              : t("knowledge.indexEconomy");
          };
          break;
      }
    });
    return newColumns;
  };

  /**
   * 搜索栏格式化（直接使用固定搜索字段）
   */
  const searchColumnsFormat = (_columns: PageColumn[]) => {
    // 覆盖原有搜索列，使用固定配置
    return fixedColumns.value.searchColumns;
  };

  return {
    api,
    auth,
    listColumnsFormat, // 固定表格列
    searchColumnsFormat, // 固定搜索列
    tableBarButtonsProps, // 标题栏按钮
    operationButtonsProps // 行操作按钮
  };
}
