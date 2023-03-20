function addModalListeners() {
	const mOpen = document.querySelectorAll('[data-modal]');
	if (mOpen.length == 0) return;
	const mClose = document.querySelectorAll('[data-close]');
	for (let el of mOpen) {
		console.log(el);
		el.addEventListener('click', modalListener);
	}
	for (let el of mClose) {
		el.addEventListener('click', modalClose);
	}
	document.addEventListener('keydown', modalClose);
};

function modalListener(e){
	let modalId = e.target.dataset.modal,
	modal = document.getElementById(modalId);
	modalShow(modal);
};

function modalShow(modal){
	const overlay = document.querySelector('.overlay');
	overlay.classList.remove('fadeOut');
	overlay.classList.add('fadeIn');
	if (modal.classList.contains('dlg-modal-fade')) {
		modal.classList.remove('fadeOut');
		modal.classList.remove('first-open');
		modal.classList.add('fadeIn');
	} else if (modal.classList.contains('dlg-modal-slide-top')) {
		modal.classList.remove('slideOutUp');
		modal.classList.add('slideInDown');
	}
	else if (modal.classList.contains('dlg-modal-slide-right')) {
		modal.classList.remove('slideOutLeft');
		modal.classList.add('slideInRight');
	}
	mStatus = true;
}

function modalClose(event) {
	const overlay = document.querySelector('.overlay'),
	modals = document.querySelectorAll('.dlg-modal');
	if (event.type != 'keydown' || event.keyCode === 27 ) {
		for (let modal of modals) {
			if (modal.classList.contains('dlg-modal-fade')) {
				modal.classList.remove('fadeIn');
				if (!(modal.classList.contains('first-open')))
					modal.classList.add('fadeOut');
			} else if (modal.classList.contains('dlg-modal-slide-top')) {
				modal.classList.remove('slideInDown');
				modal.classList.add('slideOutUp');
			} else if (modal.classList.contains('dlg-modal-slide-right')) {
				modal.classList.remove('slideInRight');
				modal.classList.add('slideOutLeft');
			}
		}
		overlay.classList.remove('fadeIn');
		overlay.classList.add('fadeOut');
		mStatus = false;
	}
}