// BMS - Bricks Management System - Main JS

// ---- Global AJAX setup ----
$(function(){
    $.ajaxSetup({
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        statusCode: {
            401: function(){ window.location.href='/login'; }
        }
    });
});

// ---- Alert System ----
function showAlert(type, message) {
    let container = document.querySelector('.alert-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'alert-container';
        document.body.appendChild(container);
    }
    const icons = { success:'bi-check-circle-fill', error:'bi-x-circle-fill', warning:'bi-exclamation-triangle-fill', info:'bi-info-circle-fill' };
    const alertEl = document.createElement('div');
    alertEl.className = `bms-alert alert-${type}`;
    alertEl.innerHTML = `<i class="bi ${icons[type]||icons.info}"></i> ${message}`;
    container.appendChild(alertEl);
    setTimeout(() => { alertEl.style.transition='opacity 0.3s'; alertEl.style.opacity='0'; setTimeout(()=>alertEl.remove(),300); }, 3500);
}

// ---- Confirm Delete ----
function confirmDelete(url, onSuccess) {
    if (!confirm('Are you sure you want to delete this record?')) return;
    $.ajax({ url, method:'POST',
        success: function(res) {
            if (res.success) { showAlert('success', res.message); if (typeof onSuccess==='function') onSuccess(); }
            else showAlert('error', res.message||'Delete failed');
        },
        error: function() { showAlert('error','Server error. Please try again.'); }
    });
}

// ---- Status badge ----
function statusBadge(status) {
    if (!status) return '--';
    const cls = `status-badge badge-${status.replace(/ /g,'_').toLowerCase()}`;
    const label = status.replace(/_/g,' ').replace(/\b\w/g, c=>c.toUpperCase());
    return `<span class="${cls}">${label}</span>`;
}

// ---- Action buttons ----
function editBtn(onclick)   { return `<button class="btn-action btn-edit me-1" onclick="${onclick}"><i class="bi bi-pencil-square"></i> Edit</button>`; }
function deleteBtn(onclick) { return `<button class="btn-action btn-delete" onclick="${onclick}"><i class="bi bi-trash"></i> Del</button>`; }
function viewBtn(onclick)   { return `<button class="btn-action btn-view me-1" onclick="${onclick}"><i class="bi bi-eye"></i></button>`; }

// ---- Format helpers ----
function fmtDate(d) { if (!d) return '--'; return d.split('T')[0]||d; }
function fmtCurrency(n) { if (n===null||n===undefined||n==='') return 'Rs. 0'; return 'Rs. '+parseFloat(n).toLocaleString('en-PK',{minimumFractionDigits:0}); }

// ---- Table states ----
function tableLoading(tbodyId, cols) {
    document.getElementById(tbodyId).innerHTML = `<tr><td colspan="${cols}" class="loading-spinner"><span class="spinner-border spinner-border-sm text-secondary"></span> Loading...</td></tr>`;
}
function tableEmpty(tbodyId, cols, msg) {
    document.getElementById(tbodyId).innerHTML = `<tr><td colspan="${cols}" class="text-center py-4 text-muted"><i class="bi bi-inbox fs-3 d-block mb-2"></i>${msg||'No records found'}</td></tr>`;
}

// ---- Modal helpers ----
function openModal(id)  { new bootstrap.Modal(document.getElementById(id)).show(); }
function closeModal(id) { const m=bootstrap.Modal.getInstance(document.getElementById(id)); if(m) m.hide(); }
function resetForm(id)  { const f=document.getElementById(id); if(f) f.reset(); }

// ============================================================
//  PAGINATION ENGINE
//  Usage:
//    BmsPager.init('myPager', data, renderFn, {perPage:25})
//    BmsPager.render('myPager')   — re-renders current page
// ============================================================
const BmsPager = (function() {
    const _instances = {};

    function init(id, data, renderFn, opts) {
        opts = opts || {};
        _instances[id] = {
            data:     data,
            filtered: data,
            renderFn: renderFn,
            page:     1,
            perPage:  opts.perPage || 10,
            searchKey: opts.searchKey || null,   // field names array to search in
        };
        _render(id);
    }

    function search(id, query) {
        const inst = _instances[id];
        if (!inst) return;
        if (!query) {
            inst.filtered = inst.data;
        } else {
            const q = query.toLowerCase();
            inst.filtered = inst.data.filter(function(row) {
                if (inst.searchKey && inst.searchKey.length) {
                    return inst.searchKey.some(k => String(row[k]||'').toLowerCase().includes(q));
                }
                // search all string fields
                return Object.values(row).some(v => String(v||'').toLowerCase().includes(q));
            });
        }
        inst.page = 1;
        _render(id);
    }

    function goPage(id, p) {
        const inst = _instances[id];
        if (!inst) return;
        const total = Math.ceil(inst.filtered.length / inst.perPage) || 1;
        inst.page = Math.max(1, Math.min(p, total));
        _render(id);
    }

    function setPerPage(id, n) {
        const inst = _instances[id];
        if (!inst) return;
        inst.perPage = parseInt(n);
        inst.page = 1;
        _render(id);
    }

    function _render(id) {
        const inst = _instances[id];
        if (!inst) return;

        const total    = inst.filtered.length;
        const perPage  = inst.perPage;
        const totalPgs = Math.ceil(total / perPage) || 1;
        const page     = inst.page;
        const start    = (page-1)*perPage;
        const slice    = inst.filtered.slice(start, start+perPage);

        // call the page's render function with current slice + start offset
        inst.renderFn(slice, start);

        // build pagination bar
        const barEl = document.getElementById('pager-bar-'+id);
        const infoEl = document.getElementById('pager-info-'+id);
        if (!barEl) return;

        const from = total ? start+1 : 0;
        const to   = Math.min(start+perPage, total);
        if (infoEl) infoEl.textContent = `Showing ${from}–${to} of ${total} records`;

        let html = '';
        // Prev
        html += `<li class="page-item ${page<=1?'disabled':''}">
            <a class="page-link" href="#" onclick="BmsPager.goPage('${id}',${page-1});return false;">&#8249;</a></li>`;

        // page numbers — show max 5 around current
        const range = _pageRange(page, totalPgs);
        if (range[0] > 1) {
            html += `<li class="page-item"><a class="page-link" href="#" onclick="BmsPager.goPage('${id}',1);return false;">1</a></li>`;
            if (range[0] > 2) html += `<li class="page-item disabled"><span class="page-link">…</span></li>`;
        }
        range.forEach(function(p) {
            html += `<li class="page-item ${p===page?'active':''}">
                <a class="page-link" href="#" onclick="BmsPager.goPage('${id}',${p});return false;">${p}</a></li>`;
        });
        if (range[range.length-1] < totalPgs) {
            if (range[range.length-1] < totalPgs-1) html += `<li class="page-item disabled"><span class="page-link">…</span></li>`;
            html += `<li class="page-item"><a class="page-link" href="#" onclick="BmsPager.goPage('${id}',${totalPgs});return false;">${totalPgs}</a></li>`;
        }

        // Next
        html += `<li class="page-item ${page>=totalPgs?'disabled':''}">
            <a class="page-link" href="#" onclick="BmsPager.goPage('${id}',${page+1});return false;">&#8250;</a></li>`;

        barEl.innerHTML = html;
    }

    function _pageRange(current, total) {
        const delta = 2;
        let start = Math.max(1, current-delta);
        let end   = Math.min(total, current+delta);
        if (end-start < 4) {
            if (start===1) end = Math.min(total, start+4);
            else start = Math.max(1, end-4);
        }
        const range = [];
        for (let i=start; i<=end; i++) range.push(i);
        return range;
    }

    function getFiltered(id) {
        const inst = _instances[id];
        return inst ? inst.filtered : [];
    }

    function getInstance(id) {
        return _instances[id];
    }

    return { init, search, goPage, setPerPage, getFiltered, getInstance };
})();

// ============================================================
//  PAGINATION BAR HTML helper — paste once per table
//  id      = unique pager id
//  cols    = colspan for centering
// ============================================================
function pagerBar(id) {
    return `
    <div class="pager-wrap d-flex align-items-center justify-content-between flex-wrap px-3 py-2 border-top">
        <div class="d-flex align-items-center gap-2">
            <span class="text-muted" style="font-size:12px">Rows:</span>
            <select class="form-select form-select-sm pager-size" style="width:75px"
                onchange="BmsPager.setPerPage('${id}', this.value)">
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
                <option value="200">200</option>
            </select>
            <span class="text-muted ms-2" id="pager-info-${id}" style="font-size:12px"></span>
        </div>
        <ul class="pagination pagination-sm mb-0" id="pager-bar-${id}"></ul>
    </div>`;
}

// search bar html helper
function searchBar(id, placeholder) {
    return `<input type="text" class="form-control form-control-sm" style="width:200px"
        placeholder="${placeholder||'Search...'}"
        oninput="BmsPager.search('${id}', this.value)">`;
}

// ============================================================
//  EXPORT ENGINE
//  Usage: exportBar('myPager', 'employees', 'myTableId') — dropdown
//  button next to the search bar; exports EXACTLY what the table
//  shows on screen (same columns, same order, same labels) across
//  all search-filtered rows/pages to JSON/XML/CSV/TXT/SQL/Excel/PDF.
// ============================================================
function exportBar(id, filename, tableId) {
    filename = filename || id;
    tableId = tableId || '';
    return `
    <div class="dropdown d-inline-block">
        <button class="btn btn-outline-secondary btn-sm dropdown-toggle" type="button"
            data-bs-toggle="dropdown" aria-expanded="false" title="Export">
            <i class="bi bi-download"></i>
        </button>
        <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','json');return false;">JSON</a></li>
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','xml');return false;">XML</a></li>
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','csv');return false;">CSV</a></li>
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','txt');return false;">TXT</a></li>
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','sql');return false;">SQL</a></li>
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','xls');return false;">MS-Excel</a></li>
            <li><a class="dropdown-item" href="#" onclick="BmsExport.run('${id}','${filename}','${tableId}','pdf');return false;">PDF</a></li>
        </ul>
    </div>`;
}

// Column header labels that are pure action/media columns — never exportable
// (icon-only buttons, thumbnails). Matched case-insensitively against <th> text.
const BMS_EXPORT_SKIP_HEADERS = ['edit', 'delete', 'actions', 'mark paid', 'slip', 'aadhaar card'];

const BmsExport = (function() {

    // Re-render every filtered row (not just the current page) off-screen
    // using the table's own renderFn, then read the resulting DOM —
    // guarantees the export matches on-screen formatting exactly.
    function _extractTableData(pagerId, tableId) {
        const inst = BmsPager.getInstance(pagerId);
        if (!inst) return null;

        const table = tableId ? document.getElementById(tableId) : null;
        const theadRow = table ? table.querySelector('thead tr') : null;
        if (!table || !theadRow) return null;

        const headerCells = Array.from(theadRow.children);
        const keepIdx = headerCells.map((th, i) => {
            const label = th.textContent.trim();
            const skip = BMS_EXPORT_SKIP_HEADERS.some(s => label.toLowerCase() === s);
            return skip ? -1 : i;
        }).filter(i => i !== -1);
        const headers = keepIdx.map(i => headerCells[i].textContent.trim());

        const tbody = table.querySelector('tbody');
        const originalHtml = tbody.innerHTML;

        // Render the FULL filtered dataset (all pages) into the live tbody momentarily,
        // read it, then restore the original (current page) view.
        inst.renderFn(inst.filtered, 0);
        const trs = Array.from(tbody.querySelectorAll('tr'));
        const rows = trs.map(tr => {
            const cells = Array.from(tr.children);
            return keepIdx.map(i => (cells[i] ? cells[i].textContent.replace(/\s+/g,' ').trim() : ''));
        }).filter(r => r.some(v => v !== ''));

        tbody.innerHTML = originalHtml;

        return { headers, rows };
    }

    function _download(content, filename, mime) {
        const blob = new Blob([content], {type: mime});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = filename;
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    function _esc(v) { return v === null || v === undefined ? '' : String(v); }
    function _escXml(v) { return _esc(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
    function _escCsv(v) { const s = _esc(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g,'""') + '"' : s; }
    function _escSqlStr(v) { return "'" + _esc(v).replace(/'/g, "''") + "'"; }
    function _slug(h) { return h.toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_|_$/g,'') || 'col'; }

    function _asObjects(headers, rows) {
        const keys = headers.map(_slug);
        return rows.map(r => {
            const o = {};
            keys.forEach((k,i) => o[k] = r[i]);
            return o;
        });
    }

    function toJson(headers, rows) {
        return JSON.stringify(_asObjects(headers, rows), null, 2);
    }

    function toXml(headers, rows, rootName) {
        rootName = rootName || 'records';
        const itemName = rootName.endsWith('s') ? rootName.slice(0,-1) : 'item';
        const keys = headers.map(_slug);
        let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<${rootName}>\n`;
        rows.forEach(r => {
            xml += `  <${itemName}>\n`;
            keys.forEach((k,i) => { xml += `    <${k}>${_escXml(r[i])}</${k}>\n`; });
            xml += `  </${itemName}>\n`;
        });
        xml += `</${rootName}>`;
        return xml;
    }

    function toCsv(headers, rows) {
        let out = headers.map(_escCsv).join(',') + '\n';
        rows.forEach(r => { out += r.map(_escCsv).join(',') + '\n'; });
        return out;
    }

    function toTxt(headers, rows) {
        const widths = headers.map((h,i) => Math.max(h.length, ...rows.map(r => _esc(r[i]).length), 3));
        const line = (vals) => vals.map((v,i) => String(v).padEnd(widths[i])).join('  |  ');
        let out = line(headers) + '\n';
        out += widths.map(w => '-'.repeat(w)).join('--+--') + '\n';
        rows.forEach(r => { out += line(r) + '\n'; });
        return out;
    }

    function toSql(headers, rows, tableName) {
        if (!rows.length) return `-- No data to export for ${tableName}`;
        const keys = headers.map(_slug);
        let out = `-- Export of ${tableName}\n`;
        rows.forEach(r => {
            const vals = r.map(v => {
                if (v === '' || v === null || v === undefined) return 'NULL';
                if (/^-?\d+(\.\d+)?$/.test(v)) return v;
                return _escSqlStr(v);
            });
            out += `INSERT INTO ${tableName} (${keys.join(', ')}) VALUES (${vals.join(', ')});\n`;
        });
        return out;
    }

    function toXlsHtml(headers, rows) {
        let out = `<html><head><meta charset="UTF-8"></head><body><table border="1">\n<tr>`;
        out += headers.map(h => `<th>${_escXml(h)}</th>`).join('') + '</tr>\n';
        rows.forEach(r => { out += '<tr>' + r.map(v => `<td>${_escXml(v)}</td>`).join('') + '</tr>\n'; });
        out += '</table></body></html>';
        return out;
    }

    function toPdf(headers, rows, title) {
        const { jsPDF } = window.jspdf;
        const orientation = headers.length > 6 ? 'landscape' : 'portrait';
        const doc = new jsPDF({ orientation, unit: 'pt', format: 'a4' });
        doc.setFontSize(14);
        doc.text(title, 40, 30);
        doc.autoTable({
            head: [headers],
            body: rows,
            startY: 45,
            styles: { fontSize: 8, cellPadding: 4 },
            headStyles: { fillColor: [240,240,240], textColor: 20, fontStyle: 'bold' },
            theme: 'grid',
        });
        doc.save(title + '.pdf');
    }

    function run(pagerId, filename, tableId, format) {
        const extracted = _extractTableData(pagerId, tableId);
        if (!extracted || !extracted.rows.length) {
            if (typeof showAlert==='function') showAlert('warning','No data to export.');
            return;
        }
        const { headers, rows } = extracted;

        if (format === 'json') {
            _download(toJson(headers, rows), filename+'.json', 'application/json');
        } else if (format === 'xml') {
            _download(toXml(headers, rows, filename), filename+'.xml', 'application/xml');
        } else if (format === 'csv') {
            _download(toCsv(headers, rows), filename+'.csv', 'text/csv');
        } else if (format === 'txt') {
            _download(toTxt(headers, rows), filename+'.txt', 'text/plain');
        } else if (format === 'sql') {
            _download(toSql(headers, rows, filename), filename+'.sql', 'text/plain');
        } else if (format === 'xls') {
            _download(toXlsHtml(headers, rows), filename+'.xls', 'application/vnd.ms-excel');
        } else if (format === 'pdf') {
            if (!window.jspdf) { if (typeof showAlert==='function') showAlert('error','PDF library failed to load.'); return; }
            toPdf(headers, rows, filename);
        }
    }

    return { run };
})();
