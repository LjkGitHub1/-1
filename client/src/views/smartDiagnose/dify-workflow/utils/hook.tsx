import { ref } from "vue";
import { message } from "@/utils/message";
import { difyWorkflowApi, type DifyWorkflowRequest } from "./api";
import { systemUploadFileApi } from "@/api/system/file";
import type { ListResult } from "@/api/types";

export interface FileItem {
  pk: number;
  filename: string;
  filesize: number;
  filepath: string;
  access_url: string;
  file_type?: string;
}

export function useDifyWorkflow() {
  const loading = ref(false);
  const fileList = ref<FileItem[]>([]);
  const selectedFiles = ref<number[]>([]);
  const workflowResult = ref<any>(null);
  const workflowError = ref<string>("");

  // 获取文件列表
  const fetchFileList = async () => {
    try {
      loading.value = true;
      const response = (await systemUploadFileApi.list({
        is_upload: true,
        page_size: 1000 // 獲取所有已上傳的文件
      })) as ListResult<FileItem>;
      if (response.code === 1000) {
        fileList.value = response.data.results || [];
      }
    } catch (error) {
      message("獲取文件列表失敗", { type: "error" });
      console.error(error);
    } finally {
      loading.value = false;
    }
  };

  // 切换文件选择状态
  const toggleFileSelection = (fileId: number) => {
    const index = selectedFiles.value.indexOf(fileId);
    if (index > -1) {
      selectedFiles.value.splice(index, 1);
    } else {
      selectedFiles.value.push(fileId);
    }
  };

  // 全选/取消全选（此函數由前端表格組件處理，這裡保留用於其他場景）
  const toggleSelectAll = () => {
    if (selectedFiles.value.length === fileList.value.length) {
      selectedFiles.value = [];
    } else {
      selectedFiles.value = fileList.value.map(file => file.pk);
    }
  };

  // 调用 Dify 工作流
  const runWorkflow = async (inputs?: Record<string, any>) => {
    if (selectedFiles.value.length === 0) {
      message("請至少選擇一個文件", { type: "warning" });
      return;
    }

    try {
      loading.value = true;
      workflowResult.value = null;
      workflowError.value = "";

      const requestData: DifyWorkflowRequest = {
        file_ids: selectedFiles.value,
        inputs: inputs || {}
      };

      const response = await difyWorkflowApi.runWorkflow(requestData);

      if (response.code === 1000) {
        workflowResult.value = response.data;
        message("工作流執行成功", { type: "success" });
      } else {
        workflowError.value = response.detail || "執行失敗";
        message(response.detail || "工作流執行失敗", { type: "error" });
      }
    } catch (error: any) {
      workflowError.value = error?.detail || error?.message || "執行失敗";
      message("工作流執行失敗", { type: "error" });
      console.error(error);
    } finally {
      loading.value = false;
    }
  };

  // 清空选择
  const clearSelection = () => {
    selectedFiles.value = [];
    workflowResult.value = null;
    workflowError.value = "";
  };

  return {
    loading,
    fileList,
    selectedFiles,
    workflowResult,
    workflowError,
    fetchFileList,
    toggleFileSelection,
    toggleSelectAll,
    runWorkflow,
    clearSelection
  };
}
