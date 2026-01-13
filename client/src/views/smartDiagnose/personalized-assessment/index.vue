<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { usePersonalizedAssessment } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnosePersonalizedAssessment"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = usePersonalizedAssessment(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.personalizedAssessment"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
