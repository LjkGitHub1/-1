<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useAssessmentDataset } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseAssessmentDataset"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useAssessmentDataset(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.assessmentDataset"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
