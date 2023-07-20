$(document).ready(function() {
    $('.game-select').select2({
        theme: "bootstrap-5",
        placeholder: 'Введите название игры',
        language: 'rus',
        minimumInputLength: 1,
        allowClear: true,
        width: '100%',
        class: 'form-control',
    });
    });
