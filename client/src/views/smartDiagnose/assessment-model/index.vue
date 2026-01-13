<script lang="ts" setup>
import { RePlusPage } from "@/components/RePlusPage";
import { useAssessmentModel } from "./utils/hook";
import { ref } from "vue";

defineOptions({
  name: "SmartDiagnoseAssessmentModel"
});

const tableRef = ref();
const {
  api,
  auth,
  operationButtonsProps,
  listColumnsFormat,
  searchColumnsFormat
} = useAssessmentModel(tableRef);
</script>

<template>
  <RePlusPage
    ref="tableRef"
    :api="api"
    :auth="auth"
    locale-name="smartDiagnose.assessmentModel"
    :search-columns-format="searchColumnsFormat"
    :list-columns-format="listColumnsFormat"
    :operationButtonsProps="operationButtonsProps"
  />
</template>
