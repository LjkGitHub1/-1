<template>
  <div v-loading="loading" class="dify-workflow-container">
    <div class="page-header mb-4">
      <div class="header-content">
        <h2 class="page-title">Dify 工作流</h2>
        <div class="header-actions">
          <el-button
            type="primary"
            :disabled="selectedFiles.length === 0"
            @click="handleRunWorkflow"
          >
            <template #icon
              ><el-icon><Play /></el-icon
            ></template>
            执行工作流
          </el-button>
          <el-button
            :disabled="selectedFiles.length === 0"
            @click="clearSelection"
          >
            <template #icon
              ><el-icon><Refresh /></el-icon
            ></template>
            清空选择
          </el-button>
          <el-button @click="fetchFileList">
            <template #icon
              ><el-icon><Refresh /></el-icon
            ></template>
            刷新列表
          </el-button>
        </div>
      </div>
    </div>

    <div class="workflow-content">
      <!-- 文件選擇區域 -->
      <el-card class="file-selection-card mb-6" shadow="never">
        <template #header>
          <div class="card-header">
            <span>文件选择</span>
            <el-checkbox
              :model-value="
                selectedFiles.length === fileList.length && fileList.length > 0
              "
              :indeterminate="
                selectedFiles.length > 0 &&
                selectedFiles.length < fileList.length
              "
              @change="handleToggleSelectAll"
            >
              全选
            </el-checkbox>
          </div>
        </template>

        <el-table
          ref="fileTableRef"
          :data="fileList"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="filename" label="文件名" min-width="200" />
          <el-table-column prop="file_type" label="文件类型" width="120">
            <template #default="{ row }">
              <el-tag v-if="row.file_type" size="small">{{
                row.file_type
              }}</el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="filesize" label="文件大小" width="120">
            <template #default="{ row }">
              {{ formatBytes(row.filesize) }}
            </template>
          </el-table-column>
          <el-table-column prop="access_url" label="操作" width="120">
            <template #default="{ row }">
              <el-link :href="row.access_url" target="_blank" type="primary">
                查看
              </el-link>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="fileList.length === 0" class="empty-state">
          <el-empty description="暂无文件，请先上传文件" />
        </div>
      </el-card>

      <!-- 結果展示區域 -->
      <el-card
        v-if="workflowResult || workflowError"
        class="result-card"
        shadow="never"
      >
        <template #header>
          <span>执行结果</span>
        </template>

        <div v-if="workflowError" class="error-result">
          <el-alert
            :title="workflowError"
            type="error"
            :closable="false"
            show-icon
          />
        </div>

        <div v-if="workflowResult" class="success-result">
          <el-alert
            title="工作流执行成功"
            type="success"
            :closable="false"
            show-icon
            class="mb-4"
          />
          <el-descriptions :column="1" border>
            <el-descriptions-item label="任务ID">
              {{ workflowResult.task_id || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag
                :type="workflowResult.status === 'success' ? 'success' : 'info'"
              >
                {{ workflowResult.status }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>

          <div v-if="workflowResult.result" class="result-content mt-4">
            <div class="result-header">
              <h4>结果內容：</h4>
              <el-button
                type="primary"
                :icon="Download"
                :loading="downloading"
                @click="handleDownloadPDF"
              >
                下载 PDF 报告
              </el-button>
            </div>
            <el-scrollbar height="500px">
              <div ref="resultContentRef" class="result-display">
                <div v-if="extractedText" class="result-text">
                  <div v-html="formatText(extractedText)" />
                </div>
                <div v-else class="result-json">
                  <pre>{{ formatResult(workflowResult.result) }}</pre>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from "vue";
import { formatBytes } from "@pureadmin/utils";
import { useDifyWorkflow } from "./utils/hook";
import Play from "~icons/ep/video-play";
import Refresh from "~icons/ep/refresh";
import Download from "~icons/ep/download";
import type { ElTable } from "element-plus";
import { message } from "@/utils/message";
import html2pdf from "html2pdf.js";

defineOptions({
  name: "DifyWorkflow"
});

const fileTableRef = ref<InstanceType<typeof ElTable>>();
const resultContentRef = ref<HTMLElement>();
const downloading = ref(false);

const {
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
} = useDifyWorkflow();

// 處理表格選擇變化
const handleSelectionChange = (selection: any[]) => {
  selectedFiles.value = selection.map(item => item.pk);
};

// 處理全選/取消全選
const handleToggleSelectAll = (checked: boolean) => {
  if (fileTableRef.value) {
    if (checked) {
      fileList.value.forEach(row => {
        fileTableRef.value?.toggleRowSelection(row, true);
      });
    } else {
      fileTableRef.value.clearSelection();
    }
  }
};

// 執行工作流
const handleRunWorkflow = () => {
  runWorkflow();
};

// 提取文本内容
const extractedText = computed(() => {
  if (!workflowResult.value?.result) return null;

  const result = workflowResult.value.result;

  // 尝试从 outputs.text 提取
  if (result?.outputs?.text) {
    return result.outputs.text;
  }

  // 尝试从 data.outputs.text 提取
  if (result?.data?.outputs?.text) {
    return result.data.outputs.text;
  }

  // 如果 result 本身就是字符串
  if (typeof result === "string") {
    return result;
  }

  return null;
});

// 格式化文本内容（处理 Markdown 和换行）
const formatText = (text: string) => {
  if (!text) return "";

  // 处理换行符
  let formatted = text.replace(/\\n/g, "\n");

  // 处理 Markdown 加粗 **text**
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // 处理 Markdown 标题
  formatted = formatted.replace(/^### (.*$)/gm, "<h3>$1</h3>");
  formatted = formatted.replace(/^## (.*$)/gm, "<h2>$1</h2>");
  formatted = formatted.replace(/^# (.*$)/gm, "<h1>$1</h1>");

  // 处理列表项
  formatted = formatted.replace(/^\d+\.\s+(.*$)/gm, "<li>$1</li>");

  // 将多个换行转换为段落
  formatted = formatted
    .split("\n\n")
    .map(para => {
      if (para.trim()) {
        // 如果包含列表项，包装在 ul 中
        if (para.includes("<li>")) {
          return `<ul>${para}</ul>`;
        }
        return `<p>${para}</p>`;
      }
      return "";
    })
    .join("");

  return formatted;
};

// 格式化結果顯示（用于 JSON）
const formatResult = (result: any) => {
  if (typeof result === "string") {
    return result;
  }
  return JSON.stringify(result, null, 2);
};

// 转换不支持的 CSS 颜色函数
const convertUnsupportedColors = (element: HTMLElement) => {
  // 获取所有样式表
  const styleSheets = Array.from(document.styleSheets);

  // 创建一个临时的 style 元素来覆盖不支持的颜色
  const tempStyle = document.createElement("style");
  tempStyle.textContent = `
    * {
      color: #303133 !important;
      background-color: #ffffff !important;
      border-color: #e4e7ed !important;
    }
    h1, h2, h3 {
      color: #303133 !important;
    }
    strong {
      color: #303133 !important;
    }
  `;
  element.appendChild(tempStyle);

  // 遍历所有元素，移除不支持的 CSS 属性
  const allElements = element.querySelectorAll("*");
  allElements.forEach(el => {
    const htmlEl = el as HTMLElement;
    // 移除可能包含 oklch 的 style 属性
    if (htmlEl.style) {
      const computedStyle = window.getComputedStyle(htmlEl);
      // 如果颜色是 oklch，替换为默认颜色
      if (computedStyle.color && computedStyle.color.includes("oklch")) {
        htmlEl.style.color = "#303133";
      }
      if (
        computedStyle.backgroundColor &&
        computedStyle.backgroundColor.includes("oklch")
      ) {
        htmlEl.style.backgroundColor = "#ffffff";
      }
    }
  });

  return element;
};

// 下载 PDF 报告
const handleDownloadPDF = async () => {
  if (!resultContentRef.value || !workflowResult.value?.result) {
    message("沒有可下载的內容", { type: "warning" });
    return;
  }

  try {
    downloading.value = true;

    // 创建要导出的内容
    const content = resultContentRef.value.cloneNode(true) as HTMLElement;

    // 转换不支持的 CSS 颜色
    const convertedContent = convertUnsupportedColors(content);

    // 创建一个临时的容器来包装内容
    const wrapper = document.createElement("div");
    wrapper.style.width = "210mm"; // A4 宽度
    wrapper.style.padding = "20px";
    wrapper.style.backgroundColor = "#ffffff";
    wrapper.style.color = "#303133";
    wrapper.appendChild(convertedContent);

    // 配置 PDF 选项
    const opt = {
      margin: [10, 10, 10, 10],
      filename: `评估与干预报告_${new Date().getTime()}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: "#ffffff",
        removeContainer: true
      },
      jsPDF: {
        unit: "mm",
        format: "a4",
        orientation: "portrait"
      }
    };

    // 生成并下载 PDF
    await html2pdf().set(opt).from(wrapper).save();

    message("PDF 报告下载成功", { type: "success" });
  } catch (error) {
    console.error("PDF 生成失败:", error);
    message("PDF 报告下载失败", { type: "error" });
  } finally {
    downloading.value = false;
  }
};

onMounted(() => {
  fetchFileList();
});
</script>

<style lang="scss" scoped>
.dify-workflow-container {
  padding: 20px;
}

.page-header {
  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;

    .page-title {
      margin: 0;
      font-size: 20px;
      font-weight: 600;
    }

    .header-actions {
      display: flex;
      gap: 12px;
    }
  }
}

.workflow-content {
  margin-top: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

.result-card {
  margin-top: 20px;
}

.result-content {
  .result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;

    h4 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
    }
  }
}

.result-display {
  .result-text {
    padding: 20px;
    font-size: 14px;
    line-height: 1.8;
    color: #303133;
    background-color: #fff;
    border: 1px solid #e4e7ed;
    border-radius: 4px;

    :deep(h1) {
      padding-bottom: 8px;
      margin: 20px 0 16px;
      font-size: 20px;
      font-weight: 600;
      color: #303133;
      border-bottom: 2px solid #409eff;
    }

    :deep(h2) {
      margin: 18px 0 12px;
      font-size: 18px;
      font-weight: 600;
      color: #303133;
    }

    :deep(h3) {
      margin: 16px 0 10px;
      font-size: 16px;
      font-weight: 600;
      color: #606266;
    }

    :deep(p) {
      margin: 12px 0;
      text-align: justify;
    }

    :deep(ul) {
      padding-left: 24px;
      margin: 12px 0;

      li {
        margin: 8px 0;
        list-style-type: disc;
      }
    }

    :deep(strong) {
      font-weight: 600;
      color: #303133;
    }
  }

  .result-json {
    padding: 16px;
    font-family: "Courier New", monospace;
    font-size: 14px;
    line-height: 1.6;
    word-wrap: break-word;
    white-space: pre-wrap;
    background-color: #f5f7fa;
    border-radius: 4px;

    pre {
      margin: 0;
    }
  }
}

.error-result {
  margin-bottom: 16px;
}

.success-result {
  .el-descriptions {
    margin-top: 16px;
  }
}
</style>
