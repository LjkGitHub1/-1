<template>
  <div class="chat-qa-container">
    <!-- 页面头部（复用现有RePlusPage组件） -->
    <RePlusPage.PageHeader
      :title="$t('smartDiagnose.chatQa.title')"
      :sub-title="$t('smartDiagnose.chatQa.pageHelp')"
      icon="icon-chat"
    />

    <!-- 主内容区（使用ReCard保持风格统一） -->
    <el-card class="mt-4">
      <!-- 模型选择栏 -->
      <div class="model-select-bar">
        <span class="label"
          >{{ $t("smartDiagnose.chatQa.chooseModel") }}：</span
        >
        <ElSelect
          v-model="state.selectedModelId"
          :placeholder="t('smartDiagnose.chatQa.chooseModelPlaceholder')"
          class="model-selector"
          :disabled="state.modelLoading"
        >
          <ElSkeleton v-if="state.modelLoading" :count="3" height="32" />
          <ElOption
            v-for="model in state.modelList"
            :key="model.id"
            :label="model.name"
            :value="model.id"
          >
            <template #default>
              <div class="model-option">
                <span class="model-name">{{ model.name }}</span>
                <span class="model-desc">{{ model.desc }}</span>
              </div>
            </template>
          </ElOption>
        </ElSelect>

        <!-- 当前用户信息（复用userStore） -->
        <div class="current-user">
          <span class="user-label"
            >{{ $t("smartDiagnose.chatQa.currentUser") }}：</span
          >
          <span class="user-name">{{
            userStore.nickname || userStore.username
          }}</span>
        </div>
      </div>

      <!-- 对话内容区（带滚动条） -->
      <div class="chat-content-wrapper">
        <ElScrollbar class="chat-scrollbar">
          <!-- 加载状态 -->
          <div v-if="state.historyLoading" class="loading-state">
            <ElSkeleton :count="4" :rows="2" />
          </div>

          <!-- 空状态 -->
          <div v-else-if="state.chatList.length === 0" class="empty-state">
            <div class="empty-icon">
              <ChatDotRound class="icon" />
            </div>
            <div class="empty-text">
              {{ $t("smartDiagnose.chatQa.emptyHint") }}
            </div>
          </div>

          <!-- 对话列表 -->
          <div v-else class="chat-list">
            <div
              v-for="msg in state.chatList"
              :key="msg.id"
              :class="['chat-item', `chat-item-${msg.role}`]"
            >
              <!-- 头像 -->
              <div class="avatar">
                <span>{{ msg.role === "user" ? "U" : "AI" }}</span>
              </div>

              <!-- 消息内容 -->
              <div class="message-content">
                <div class="message-meta">
                  <span class="model-tag">{{ msg.modelName }}</span>
                  <span class="time">{{ msg.timestamp }}</span>
                </div>
                <div class="message-text">{{ msg.content }}</div>
              </div>
            </div>
          </div>
        </ElScrollbar>
      </div>

      <div class="input-area">
        <ElInput
          v-model="state.inputContent"
          :rows="4"
          :placeholder="$t('smartDiagnose.chatQa.inputPlaceholder')"
          :disabled="state.sending || !state.selectedModelId"
          @keydown.enter.exact="sendQuestion"
          @keydown.enter.shift="() => {}"
        />
        <div class="input-actions">
          <ElButton
            type="primary"
            :loading="state.sending"
            :disabled="
              !state.inputContent.trim() ||
              !state.selectedModelId ||
              state.sending
            "
            @click="sendQuestion"
          >
            {{ $t("common.send") }}
            <Position class="ml-1" />
          </ElButton>
        </div>
      </div>
    </el-card>
  </div>
</template>
<!--  -->

<script lang="ts" setup>
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { RePlusPage } from "@/components/RePlusPage";
// import ReCard from "@/components/ReCard.vue";
import {
  ElSelect,
  ElOption,
  ElScrollbar,
  ElInput,
  ElButton,
  ElSkeleton
} from "element-plus";
import { useChatQa } from "./utils/hook";
import { useUserStoreHook } from "@/store/modules/user";
import ChatDotRound from "~icons/ep/chat-dot-round";
import Position from "~icons/ep/position";

// 组件命名规范（与现有组件一致）
defineOptions({
  name: "SmartDiagnoseChatQaPage"
});

// 初始化
const { t } = useI18n();
const userStore = useUserStoreHook();
const { state, init, sendQuestion } = useChatQa();

// 页面加载时初始化数据
onMounted(() => {
  // init();
});
</script>

<style scoped lang="scss">
.chat-qa-container {
  padding: 0 20px 20px;
}

.model-select-bar {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #eee;

  .label {
    margin-right: 8px;
    font-size: 14px;
    color: #666;
  }

  .model-selector {
    width: 300px;
    margin-right: 20px;
  }

  .model-option {
    .model-name {
      font-weight: 500;
    }

    .model-desc {
      margin-top: 4px;
      font-size: 12px;
      color: #999;
    }
  }

  .current-user {
    margin-left: auto;
    font-size: 14px;

    .user-label {
      color: #666;
    }

    .user-name {
      margin-left: 4px;
      font-weight: 500;
      color: #333;
    }
  }
}

.chat-content-wrapper {
  height: 500px;
  padding: 16px 0;

  .chat-scrollbar {
    height: 100%;
    padding: 0 10px;
  }

  .loading-state {
    padding: 20px;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #999;

    .empty-icon {
      margin-bottom: 16px;

      .icon {
        width: 64px;
        height: 64px;
        fill: #ccc;
      }
    }
  }

  .chat-list {
    .chat-item {
      display: flex;
      padding: 0 10px;
      margin-bottom: 16px;

      &.chat-item-user {
        flex-direction: row-reverse;
      }

      .avatar {
        display: flex;
        flex-shrink: 0;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        font-size: 16px;
        color: white;
        border-radius: 50%;

        & + .message-content {
          margin-left: 12px;
        }
      }

      .chat-item-user .avatar {
        background-color: #409eff;

        & + .message-content {
          margin-right: 12px;
          margin-left: 0;
        }
      }

      .chat-item-ai .avatar {
        background-color: #67c23a;
      }

      .message-content {
        max-width: 70%;

        .message-meta {
          display: flex;
          align-items: center;
          margin-bottom: 4px;
          font-size: 12px;

          .model-tag {
            padding: 2px 6px;
            margin-right: 8px;
            background-color: #f0f2f5;
            border-radius: 4px;
          }

          .time {
            color: #999;
          }
        }

        .message-text {
          padding: 8px 12px;
          line-height: 1.5;
          border-radius: 6px;
        }
      }

      .chat-item-user .message-content {
        .message-text {
          color: #1890ff;
          background-color: #e6f7ff;
        }
      }

      .chat-item-ai .message-content {
        .message-text {
          color: #237804;
          background-color: #f0fff4;
        }
      }
    }
  }
}

.input-area {
  padding: 16px 0;
  border-top: 1px solid #eee;

  .el-textarea {
    margin-bottom: 12px;
  }

  .input-actions {
    display: flex;
    justify-content: flex-end;
  }
}
</style>
