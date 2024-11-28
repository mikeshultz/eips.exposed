{{- define "eips-web.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- define "eips-web.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s-%s" .Release.Name $name "web" | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- define "eips-web.labels" -}}
helm.sh/chart: {{ include "eips-web.chart" . }}
{{ include "eips-web.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}


{{- define "eips-web.selectorLabels" -}}
app.kubernetes.io/name: {{ include "eips-web.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}




{{- define "typesense-search.chart" -}}
{{- printf "%s-search-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- define "typesense-search.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s-%s" .Release.Name $name "search" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "typesense-search.labels" -}}
helm.sh/chart: {{ include "typesense-search.chart" . }}
{{ include "typesense-search.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}


{{- define "typesense-search.selectorLabels" -}}
app.kubernetes.io/name: {{ include "typesense-search.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}



{{- define "update.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s-%s" .Release.Name $name "update" | trunc 63 | trimSuffix "-" }}
{{- end }}
