import { ref } from "vue";
import { message } from "@/utils/message";
import { artTherapyWorkflowApi, type ArtTherapyWorkflowRequest } from "./api";
import { systemUploadFileApi } from "@/api/system/file";

export interface UploadedFile {
  pk: number;
  filename: string;
  filesize: number;
  filepath: string;
  access_url: string;
  file_type?: string;
}

export function useArtTherapyWorkflow() {
  const loading = ref(false);
  const uploadedFiles = ref<UploadedFile[]>([]);
  const workflowResult = ref<any>(null);
  const workflowError = ref<string>("");

  // 上传图片文件
  const uploadImage = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await systemUploadFileApi.upload(formData);

      if (response.code === 1000 && response.data && response.data.length > 0) {
        const uploadedFile = response.data[0];
        uploadedFiles.value.push({
          pk: uploadedFile.pk,
          filename: uploadedFile.filename,
          filesize: uploadedFile.filesize,
          filepath: uploadedFile.filepath,
          access_url: uploadedFile.access_url,
          file_type: uploadedFile.file_type
        });
        message("图片上传成功", { type: "success" });
        return uploadedFile;
      } else {
        message("图片上传失败", { type: "error" });
        return null;
      }
    } catch (error) {
      console.error("Upload error:", error);
      message("图片上传失败", { type: "error" });
      return null;
    }
  };

  // 删除已上传的文件
  const removeFile = (fileId: number) => {
    const index = uploadedFiles.value.findIndex(f => f.pk === fileId);
    if (index > -1) {
      uploadedFiles.value.splice(index, 1);
    }
  };

  // 清空所有文件
  const clearFiles = () => {
    uploadedFiles.value = [];
  };

  // 调用艺术治疗工作流
  const runWorkflow = async (inputs?: Record<string, any>) => {
    if (uploadedFiles.value.length === 0) {
      message("请至少上传一张图片", { type: "warning" });
      return;
    }

    try {
      loading.value = true;
      workflowResult.value = null;
      workflowError.value = "";

      const requestData: ArtTherapyWorkflowRequest = {
        file_ids: uploadedFiles.value.map(f => f.pk),
        inputs: inputs || {}
      };

      const response = await artTherapyWorkflowApi.runWorkflow(requestData);

      if (response.code === 1000) {
        workflowResult.value = response.data;
        message("工作流执行成功", { type: "success" });
      } else {
        workflowError.value = response.detail || "执行失败";
        message(response.detail || "工作流执行失败", { type: "error" });
      }
    } catch (error: any) {
      workflowError.value = error?.detail || error?.message || "执行失败";
      message("工作流执行失败", { type: "error" });
      console.error(error);
    } finally {
      loading.value = false;
    }
  };

  // 清空结果
  const clearResult = () => {
    workflowResult.value = null;
    workflowError.value = "";
  };

  return {
    loading,
    uploadedFiles,
    workflowResult,
    workflowError,
    uploadImage,
    removeFile,
    clearFiles,
    runWorkflow,
    clearResult
  };
}
